from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView, View
from devicetrack.utils import save_history_standard
from django.contrib import messages

from .models import TypePlan, TypePlanHistory
from .forms import FormTypePlan


class BaseTypePlanFormView(TemplateView, FormMixin):
    form_class = FormTypePlan
    template_name = 'type_plan_list.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object') and self.object:
            kwargs.update({'instance': self.object})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = TypePlan.objects.all().filter(status='ACTIVE').order_by('-updated_at')

        return context


class TypePlanCreateView(BaseTypePlanFormView, ProcessFormView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'El registro a sido creado correctamente')
            save_history_standard(request, form.instance, 'create')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return redirect('type_plan_list')


class TypePlanUpdateView(BaseTypePlanFormView, ProcessFormView):

    def get_object(self):
        return TypePlan.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            if form.has_changed():
                messages.success(request, 'El registro fue actualizado correctamente')
                save_history_standard(request, form.instance, 'update')
                return self.form_valid(form)
            else:
                messages.info(request, 'No hubo cambios en el registro')
                return redirect('type_plan_list')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_type_plan'] = self.get_object().id_type_plan
        return context

    def form_valid(self, form):
        form.save()
        return redirect('type_plan_list')


class TypePlanToggleStatusView(View):
    def get(self, request, pk):
        instance = get_object_or_404(TypePlan, pk=pk)

        instance.status = 'INACTIVE' if instance.status == 'ACTIVE' else 'ACTIVE'
        instance.save(update_fields=['status', 'updated_at'])

        save_history_standard(request, instance, 'toggle')

        messages.success(request, 'El estado del registro fue actualizado correctamente')
        return redirect('type_plan_list')


class TypePlanDeletedRecordsView(ListView):
    model = TypePlan
    template_name = 'type_plan_list_deleted_records.html'

    def get_queryset(self):
        return TypePlan.objects.all().filter(status='INACTIVE').order_by('-updated_at')


class TypePlanHistoryView(ListView):
    model = TypePlanHistory
    template_name = 'type_plan_list_history.html'

    def get_queryset(self):
        return TypePlanHistory.objects.all().order_by('-updated_at')
