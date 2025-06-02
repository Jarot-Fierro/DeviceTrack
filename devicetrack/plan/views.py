from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView, View
from devicetrack.utils import save_history_standard
from django.contrib import messages

from .models import Plan, PlanHistory
from .forms import FormPlan, FormCancellationPlan


class BasePlanFormView(TemplateView, FormMixin):
    form_class = FormPlan
    template_name = 'plan_list.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object') and self.object:
            kwargs.update({'instance': self.object})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Plan.objects.all().filter(status='ACTIVE').order_by('-updated_at')

        return context


class PlanCreateView(BasePlanFormView, ProcessFormView):
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
        return redirect('plan_list')


class PlanUpdateView(BasePlanFormView, ProcessFormView):

    def get_object(self):
        return Plan.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()

        if form.is_valid():
            if form.has_changed():
                messages.success(request, 'El registro fue actualizado correctamente')
                save_history_standard(request, form.instance, 'update')
                return self.form_valid(form)
            else:
                messages.info(request, 'No hubo cambios en el registro')
                return redirect('plan_list')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_plan'] = self.get_object().id_plan
        return context

    def form_valid(self, form):
        form.save()
        return redirect('plan_list')


class PlanToggleStatusView(View):
    def get(self, request, pk):
        instance = get_object_or_404(Plan, pk=pk)
        old_instance = Plan.objects.get(pk=instance.pk)

        instance.status = 'INACTIVE' if instance.status == 'ACTIVE' else 'ACTIVE'
        instance.save(update_fields=['status', 'updated_at'])

        save_history_standard(request, instance, 'toggle')

        messages.success(request, 'El estado del registro fue actualizado correctamente')
        return redirect('plan_list')


class BasePlanCancellationFormView(TemplateView, FormMixin):
    form_class = FormCancellationPlan
    template_name = 'plan_cancellation.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object') and self.object:
            kwargs.update({'instance': self.object})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Plan.objects.all().filter(status='ACTIVE').order_by('-updated_at')
        context['object_list_inactive'] = Plan.objects.all().filter(status='INACTIVE').order_by('-updated_at')

        return context


class PlanCancellationUpdateView(BasePlanCancellationFormView, ProcessFormView):
    def get_object(self):
        return Plan.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            if form.has_changed():
                messages.success(request, 'El registro fue actualizado correctamente')
                save_history_standard(request, form.instance, 'cancelated plan')
                return self.form_valid(form)
            else:
                messages.info(request, 'No hubo cambios en el registro')
                return redirect('plan_list')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_plan'] = self.get_object().id_plan
        return context

    def form_valid(self, form):
        form.save()
        return redirect('plan_list')


class PlanDeletedRecordsView(ListView):
    model = Plan
    template_name = 'plan_list_deleted_records.html'

    def get_queryset(self):
        return Plan.objects.all().filter(status='INACTIVE').order_by('-updated_at')


class PlanHistoryView(ListView):
    model = PlanHistory
    template_name = 'plan_list_history.html'

    def get_queryset(self):
        return PlanHistory.objects.all().order_by('-updated_at')
