from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from article.models import Article
from computer.models import Computer
from phone.models import Phone
from printer.models import Printer
from .forms import EntryForm, OutputForm, SupportForm
from .models import Transaction, DetailTransaction, TransactionOutput, SupportTransaction
from .utils import update_status_device

# Diccionario que mapea los tipos a los modelos
DEVICE_MODELS = {
    'phone': Phone,
    'printer': Printer,
    'computer': Computer,
    'article': Article,
}


class TransactionBaseView(TemplateView):
    template_name = 'transaction_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_types'] = DEVICE_MODELS.keys()
        return context


class DeviceTransactionMixin:
    def get_device_model(self):
        tipo = self.request.GET.get('type')
        model = DEVICE_MODELS.get(tipo)
        if not model:
            raise Http404("Tipo de dispositivo no válido.")
        return model

    def get_device_queryset(self):
        model = self.get_device_model()
        if isinstance(self, EntryView):
            return model.objects.filter(status='ACTIVE', status_device='ASSIGNED')
        elif isinstance(self, OutputView):
            return model.objects.filter(status='ACTIVE', status_device='IN_STOCK')
        elif isinstance(self, SupportView):
            return model.objects.filter(status='ACTIVE')
        return model.objects.none()


class EntryView(DeviceTransactionMixin, FormView):
    template_name = 'transaction_index.html'
    form_class = EntryForm
    success_url = reverse_lazy('transaction:entry')

    def get_device_queryset(self):
        type_ = self.request.GET.get('type')
        model_map = DEVICE_MODELS
        model = model_map.get(type_)
        if model:
            return model.objects.filter(status='ACTIVE', status_device='ASSIGNED')
        return model.objects.none()  # si type no es válido

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['device'].queryset = self.get_device_queryset()
        return form

    def form_valid(self, form):
        with transaction.atomic():
            trx = Transaction.objects.create(
                type='ENTRY',
                official=form.cleaned_data['official'],
                login_user=self.request.user,
                observation=form.cleaned_data.get('observation', '')
            )
            device = form.cleaned_data['device']
            content_type = ContentType.objects.get_for_model(device.__class__)
            DetailTransaction.objects.create(
                transaction=trx,
                content_type=content_type,
                object_id=device.universal_id
            )
            update_status_device(trx, device)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = 'entry'
        tipo = self.request.GET.get('type')

        cards = [
            {'key': 'phone', 'label': 'Celulares', 'color': 'primary'},
            {'key': 'computer', 'label': 'Computadores', 'color': 'info'},
            {'key': 'printer', 'label': 'Impresoras', 'color': 'success'},
            {'key': 'article', 'label': 'Otros Artículos', 'color': 'secondary'},
        ]

        # Buscar el label según el type de la URL
        tipo_label = next((card['label'] for card in cards if card['key'] == tipo), 'Equipo')

        context.update({
            'title': 'Ingresos',
            'action': action,
            'form_partial': 'components/transaction_entry_form.html',
            'cards': cards,
            'section_name': f'Ingreso de {tipo_label}',
        })
        return context


class OutputView(DeviceTransactionMixin, FormView):
    template_name = 'transaction_index.html'
    form_class = OutputForm
    success_url = reverse_lazy('index')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['device'].queryset = self.get_device_queryset()
        return form

    def form_valid(self, form):
        with transaction.atomic():
            trx = Transaction.objects.create(
                type='OUTPUT',
                official=form.cleaned_data['official'],
                login_user=self.request.user
            )

            device = form.cleaned_data['device']
            content_type = ContentType.objects.get_for_model(device.__class__)
            DetailTransaction.objects.create(
                transaction=trx,
                content_type=content_type,
                object_id=device.universal_id
            )

            TransactionOutput.objects.create(
                transaction=trx,
                type_output=form.cleaned_data['type_output'],
                return_date=form.cleaned_data.get('return_date')
            )

            update_status_device(trx, device)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = 'output'
        tipo = self.request.GET.get('type')

        cards = [
            {'key': 'phone', 'label': 'Celulares', 'color': 'primary'},
            {'key': 'computer', 'label': 'Computadores', 'color': 'info'},
            {'key': 'printer', 'label': 'Impresoras', 'color': 'success'},
            {'key': 'article', 'label': 'Otros Artículos', 'color': 'secondary'},
        ]

        # Buscar el label según el type de la URL
        tipo_label = next((card['label'] for card in cards if card['key'] == tipo), 'Equipo')

        context.update({
            'title': 'Entregas',
            'action': action,
            'form_partial': 'components/transaction_output_form.html',
            'cards': cards,
            'section_name': f'Entrega de {tipo_label}',
        })
        return context


class SupportView(DeviceTransactionMixin, FormView):
    template_name = 'transaction_index.html'
    form_class = SupportForm
    success_url = reverse_lazy('transaction:support')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = 'support'
        tipo = self.request.GET.get('type')

        cards = [
            {'key': 'phone', 'label': 'Celulares', 'color': 'primary'},
            {'key': 'computer', 'label': 'Computadores', 'color': 'info'},
            {'key': 'printer', 'label': 'Impresoras', 'color': 'success'},
            {'key': 'article', 'label': 'Otros Artículos', 'color': 'secondary'},
        ]

        # Buscar el label según el type de la URL
        tipo_label = next((card['label'] for card in cards if card['key'] == tipo), 'Equipo')

        context.update({
            'title': 'Soporte',
            'action': action,
            'form_partial': 'components/transaction_support_form.html',
            'cards': cards,
            'section_name': f'Soporte de {tipo_label}',
        })
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['device'].queryset = self.get_device_queryset()
        return form

    def form_valid(self, form):
        with transaction.atomic():
            trx = Transaction.objects.create(
                type='SUPPORT',
                official=form.cleaned_data['official'],
                login_user=self.request.user
            )

            device = form.cleaned_data['device']
            content_type = ContentType.objects.get_for_model(device.__class__)
            SupportTransaction.objects.create(
                transaction=trx,
                type_soporte=form.cleaned_data['type_soporte'],
                login_user=self.request.user,
                date_start=form.cleaned_data['date_start'],
                date_end=form.cleaned_data.get('date_end'),
                problem=form.cleaned_data['problem'],
                solution=form.cleaned_data.get('solution'),
                content_type=content_type,
                object_id=device.universal_id
            )

            # No usamos update_status_device aquí, pero puedes hacerlo si lo deseas
        return super().form_valid(form)
