from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView, View

from devicetrack.utils import save_history_standard
from .forms import FormInks
from .models import Inks, InksHistory


class BaseInksFormView(TemplateView, FormMixin):
    form_class = FormInks
    template_name = 'inks_list.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object') and self.object:
            kwargs.update({'instance': self.object})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Inks.objects.all().filter(status='ACTIVE').order_by('-updated_at')

        return context


class InksCreateView(BaseInksFormView, ProcessFormView):
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
        return redirect('inks_list')


class InksUpdateView(BaseInksFormView, ProcessFormView):

    def get_object(self):
        return Inks.objects.get(pk=self.kwargs['pk'])

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
                return redirect('inks_list')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_inks'] = self.get_object().id_inks
        return context

    def form_valid(self, form):
        form.save()
        return redirect('inks_list')


class InksToggleStatusView(View):
    def get(self, request, pk):
        instance = get_object_or_404(Inks, pk=pk)

        instance.status = 'INACTIVE' if instance.status == 'ACTIVE' else 'ACTIVE'
        instance.save(update_fields=['status', 'updated_at'])

        save_history_standard(request, instance, 'toggle')

        messages.success(request, 'El estado del registro fue actualizado correctamente')

        if instance.status == 'ACTIVE':
            return redirect('inks_deleted_records')
        else:
            return redirect('inks_list')


class InksDeletedRecordsView(ListView):
    model = Inks
    template_name = 'inks_list_deleted_records.html'

    def get_queryset(self):
        return Inks.objects.all().filter(status='INACTIVE').order_by('-updated_at')


class InksHistoryView(ListView):
    model = InksHistory
    template_name = 'inks_list_history.html'

    def get_queryset(self):
        return InksHistory.objects.all().order_by('-updated_at')
