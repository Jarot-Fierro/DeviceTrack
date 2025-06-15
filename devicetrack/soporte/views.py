from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView, View

from devicetrack.utils import save_history_standard
from .forms import FormSoporte
from .models import Soporte, SoporteHistory


class BaseSoporteFormView(TemplateView, FormMixin):
    form_class = FormSoporte
    template_name = 'soporte_list.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object') and self.object:
            kwargs.update({'instance': self.object})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Soporte.objects.all().filter(status='ACTIVE').order_by('-updated_at')

        return context


class SoporteCreateView(BaseSoporteFormView, ProcessFormView):
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
        return redirect('soporte_list')


class SoporteUpdateView(BaseSoporteFormView, ProcessFormView):

    def get_object(self):
        return Soporte.objects.get(pk=self.kwargs['pk'])

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
                return redirect('soporte_list')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_soporte'] = self.get_object().id_soporte
        return context

    def form_valid(self, form):
        form.save()
        return redirect('soporte_list')


class SoporteToggleStatusView(View):
    def get(self, request, pk):
        instance = get_object_or_404(Soporte, pk=pk)

        instance.status = 'INACTIVE' if instance.status == 'ACTIVE' else 'ACTIVE'
        instance.save(update_fields=['status', 'updated_at'])

        save_history_standard(request, instance, 'toggle')

        messages.success(request, 'El estado del registro fue actualizado correctamente')

        if instance.status == 'ACTIVE':
            return redirect('soporte_deleted_records')
        else:
            return redirect('soporte_list')


class SoporteDeletedRecordsView(ListView):
    model = Soporte
    template_name = 'soporte_list_deleted_records.html'

    def get_queryset(self):
        return Soporte.objects.all().filter(status='INACTIVE').order_by('-updated_at')


class SoporteHistoryView(ListView):
    model = SoporteHistory
    template_name = 'soporte_list_history.html'

    def get_queryset(self):
        return SoporteHistory.objects.all().order_by('-updated_at')
