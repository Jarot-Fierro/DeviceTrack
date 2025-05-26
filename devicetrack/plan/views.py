from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView, View
from django.forms.models import model_to_dict
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
import json

from .models import Plan, PlanHistory
from .forms import FormPlan, FormCancellationPlan


def save_history(request, instance, old_instance, action):
    model_name = instance.__class__.__name__

    if old_instance:
        old_data = model_to_dict(old_instance)
        old_data['id_plan'] = str(old_instance.id_plan)

        old_data['name'] = str(old_instance.name)
        old_data['description'] = str(old_instance.description)

        old_data['gigabytes'] = str(old_instance.gigabytes)
        old_data['minutes'] = str(old_instance.minutes)
        old_data['messages'] = str(old_instance.messages)

        old_data['unlimited_gigabytes'] = str(old_instance.unlimited_gigabytes)
        old_data['unlimited_minutes'] = str(old_instance.unlimited_minutes)
        old_data['unlimited_messages'] = str(old_instance.unlimited_messages)

        old_data['price'] = str(old_instance.price)
        old_data['status_billing'] = str(old_instance.status_billing)
        old_data['status'] = str(old_instance.status)

        old_data['date_hiring'] = str(old_instance.date_hiring)
        old_data['date_cancellation'] = str(old_instance.date_cancellation)
        old_data['reason_cancellation'] = str(old_instance.reason_cancellation)

        old_data['type_plan'] = {
            'id': str(old_instance.type_plan.id_type_plan),
            'name': old_instance.type_plan.name,
            'status': old_instance.type_plan.status
        }
    else:
        old_data = None

    new_data = model_to_dict(instance)
    new_data['id_plan'] = str(instance.id_plan)

    new_data['name'] = str(instance.name)
    new_data['description'] = str(instance.description)

    new_data['gigabytes'] = str(instance.gigabytes)
    new_data['minutes'] = str(instance.minutes)
    new_data['messages'] = str(instance.messages)

    new_data['unlimited_gigabytes'] = str(instance.unlimited_gigabytes)
    new_data['unlimited_minutes'] = str(instance.unlimited_minutes)
    new_data['unlimited_messages'] = str(instance.unlimited_messages)

    new_data['price'] = str(instance.price)
    new_data['status_billing'] = str(instance.status_billing)
    new_data['status'] = str(instance.status)

    new_data['date_hiring'] = str(instance.date_hiring)
    new_data['date_cancellation'] = str(instance.date_cancellation)
    new_data['reason_cancellation'] = str(instance.reason_cancellation)

    new_data['type_plan'] = {
        'id_type_plan': str(instance.type_plan.id_type_plan),
        'name': instance.type_plan.name,
        'status': instance.type_plan.status
    }

    data = {
        'id_plan': str(instance.id_plan),
        'operation': action,
        'old_data': old_data if old_data else None,
        'new_data': new_data,
        'user_login_history': request.user.username if request.user.username else 'anonymous',
        'user_login': request.user if request.user.is_authenticated else None,
        'type_plan': instance.type_plan
    }
    if model_name == 'Plan':
        PlanHistory.objects.create(**data)


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
        context['object_list_inactive'] = Plan.objects.all().filter(status='INACTIVE').order_by('-updated_at')

        return context

    def change_data(self, form):
        instance = form.instance
        if instance.unlimited_gigabytes:
            instance.gigabytes = 0
        if instance.unlimited_minutes:
            instance.minutes = 0
        if instance.unlimited_messages:
            instance.messages = 0


class PlanCreateView(BasePlanFormView, ProcessFormView):
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
        old_instance = Plan.objects.get(pk=self.object.pk)

        if form.is_valid():
            if form.has_changed():
                messages.success(request, 'El registro fue actualizado correctamente')
                save_history(request, form.instance, old_instance, 'update')
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

        save_history(request, instance, old_instance, 'toggle')

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
        old_instance = Plan.objects.get(pk=self.object.pk)
        if form.is_valid():
            if form.has_changed():
                messages.success(request, 'El registro fue actualizado correctamente')
                save_history(request, form.instance, old_instance, 'update')
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


class PlanHistoryView(ListView):
    model = PlanHistory
    template_name = 'plan_list_history.html'

    def get_queryset(self):
        return PlanHistory.objects.all().order_by('-updated_at')
