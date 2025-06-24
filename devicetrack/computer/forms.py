import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from brand.models import Brand
from device_owner.models import DeviceOwner
from devicetrack.validation_forms import validate_ip
from licence_os.models import LicenceOs
from microsoft_office.models import MicrosoftOffice
from model.models import Model
from subcategory.models import SubCategory
from .models import Computer


class FormComputer(forms.ModelForm):
    number_serie = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'imei_computer',
                'class': 'form-control',
                'placeholder': 'Número de Serie',
                'min-lenght': '1',
                'max-lenght': '100'
            }),
        required=True
    )
    mac = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'mac_computer',
                'class': 'form-control',
                'placeholder': '00:1A:2B:3C:4D:5E',
                'min-lenght': '1',
                'max-lenght': '100'
            }),
        required=True
    )
    ip = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'ip_computer',
                'class': 'form-control',
                'placeholder': '192.168.0.1',
                'min-lenght': '1',
                'max-lenght': '100'
            }),
        required=True
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'brand_computer',
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
                'id': 'model_computer',
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
                'id': 'subcategory_computer',
            }
        ),
        required=True
    )
    licence_os = forms.ModelChoiceField(
        queryset=LicenceOs.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'subcategory_computer',
            }
        ),
        required=True
    )
    microsoft_office = forms.ModelChoiceField(
        queryset=MicrosoftOffice.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'subcategory_computer',
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
                'id': 'subcategory_computer',
            }
        ),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'description_licence_os',
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe más detalles aquí...'
            }),
        required=False,
        validators=[MaxLengthValidator(200, message='No puedes escribir más de 200 caracteres.')],
    )

    def clean_number_serie(self):
        number_serie = self.cleaned_data['number_serie'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Computer.objects.filter(number_serie__iexact=number_serie).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        if exists:
            raise ValidationError("Ya existe una marca con este nombre.")

        return number_serie

    def clean_ip(self):
        ip = self.cleaned_data['ip'].strip()
        validate_ip(ip)
        return ip

    def clean_mac(self):
        mac = self.cleaned_data['mac'].strip()
        if not re.match(r'^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$', mac):
            raise ValidationError("La dirección MAC no es válida. Debe tener el formato 00:1A:2B:3C:4D:5E")
        return mac

    class Meta:
        fields = [
            'number_serie',
            'mac',
            'ip',
            'brand',
            'model',
            'subcategory',
            'licence_os',
            'microsoft_office',
            'device_owner',
            'description'
        ]
        model = Computer
