from django import forms
from django.core.exceptions import ValidationError

from brand.models import Brand
from device_owner.models import DeviceOwner
from devicetrack.validation_forms import validate_ip
from inks.models import Inks
from model.models import Model
from subcategory.models import SubCategory
from .models import Printer


class FormPrinter(forms.ModelForm):
    number_serie = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'number_serie_printer',
                'class': 'form-control',
                'placeholder': 'Número de Serie',
                'minlength': '1',
                'maxlength': '100'
            }),
        required=True
    )
    hh = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'mac_printer',
                'class': 'form-control',
                'minlength': '1',
                'maxlength': '100'
            }),
        required=True
    )
    ip = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'ip_printer',
                'class': 'form-control',
                'placeholder': '192.168.0.1',
                'minlength': '1',
                'maxlength': '100'
            }),
        required=True
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'brand_printer',
            }
        ),
        required=True
    )
    model = forms.ModelChoiceField(
        queryset=Model.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'model_printer',
            }
        ),
        required=True
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'subcategory_printer',
            }
        ),
        required=True
    )
    inks = forms.ModelChoiceField(
        queryset=Inks.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'subcategory_printer',
            }
        ),
        required=True
    )
    device_owner = forms.ModelChoiceField(
        queryset=DeviceOwner.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'subcategory_printer',
            }
        ),
        required=True
    )

    def clean_number_serie(self):
        number_serie = self.cleaned_data['number_serie'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Printer.objects.filter(number_serie__iexact=number_serie).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        if exists:
            raise ValidationError("Ya existe una marca con este nombre.")

        return number_serie

    def clean_ip(self):
        ip = self.cleaned_data['ip'].strip()
        validate_ip(ip)

        return ip

    class Meta:
        fields = [
            'number_serie',
            'hh',
            'ip',
            'brand',
            'model',
            'subcategory',
            'inks',
            'device_owner',
        ]
        model = Printer
