from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView, View
from django.forms.models import model_to_dict
from django.contrib import messages

from .models import OperativeSystem, OperativeSystemHistory
from .forms import FormOperativeSystem


def save_history(request, instance, old_instance, action):
    model_name = instance.__class__.__name__

    data = {
        'id_operative_system': str(instance.id_operative_system),
        'operation': action,
        'old_data': old_instance if old_instance else None,
        'new_data': model_to_dict(instance),
        'user_login_history': request.user.username if request.user.username else 'anonymous',
        'user_login': request.user if request.user.is_authenticated else None
    }
    if model_name == 'OperativeSystem':
        OperativeSystemHistory.objects.create(**data)


class BaseOperativeSystemFormView(TemplateView, FormMixin):
    form_class = FormOperativeSystem
    template_name = 'operative_system_list.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object') and self.object:
            kwargs.update({'instance': self.object})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = OperativeSystem.objects.all().filter(status='ACTIVE').order_by('-updated_at')
        context['object_list_inactive'] = OperativeSystem.objects.all().filter(status='INACTIVE').order_by('-updated_at')

        return context


class OperativeSystemCreateView(BaseOperativeSystemFormView, ProcessFormView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'El registro a sido creado correctamente')
            save_history(request, form.instance, None, 'create')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return redirect('operative_system_list')


class OperativeSystemUpdateView(BaseOperativeSystemFormView, ProcessFormView):

    def get_object(self):
        return OperativeSystem.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        old_instance = model_to_dict(form.instance)

        if form.is_valid():
            if form.has_changed():
                messages.success(request, 'El registro fue actualizado correctamente')
                save_history(request, form.instance, old_instance, 'update')
                return self.form_valid(form)
            else:
                messages.info(request, 'No hubo cambios en el registro')
                return redirect('operative_system_list')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_operative_system'] = self.get_object().id_operative_system
        return context

    def form_valid(self, form):
        form.save()
        return redirect('operative_system_list')


class OperativeSystemToggleStatusView(View):
    def get(self, request, pk):
        instance = get_object_or_404(OperativeSystem, pk=pk)
        old_instance = model_to_dict(instance)

        instance.status = 'INACTIVE' if instance.status == 'ACTIVE' else 'ACTIVE'
        instance.save(update_fields=['status', 'updated_at'])

        save_history(request, instance, old_instance, 'toggle')

        messages.success(request, 'El estado de la sistema operativo fue actualizado correctamente')
        return redirect('operative_system_list')


class OperativeSystemHistoryView(ListView):
    model = OperativeSystemHistory
    template_name = 'operative_system_list_history.html'

    def get_queryset(self):
        return OperativeSystemHistory.objects.all().order_by('-updated_at')
