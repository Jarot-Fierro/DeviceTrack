from django import forms
from django.core.validators import MaxLengthValidator

from devicetrack.validation_forms import validate_name, validate_description, validate_default
from establishment.models import Establishment
from .models import Departament


class FormDepartament(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_departament',
                'class': 'form-control',
                'placeholder': 'Nombre del Departamento',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'address_departament',
                'class': 'form-control',
                'placeholder': 'Calle y número',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    establishment = forms.ModelChoiceField(
        queryset=Establishment.objects.all().filter(status='ACTIVE'),
        empty_label='Seleccione una Opción',
        widget=forms.Select(
            attrs={
                'id': 'establishment_departament',
                'class': 'form-control'
            }),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'description_brand',
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe más detalles aquí...'
            }),
        required=False,
        validators=[MaxLengthValidator(200, message='No puedes escribir más de 200 caracteres.')],
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Departament.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(name, exists, 'nombre del departamento')

        return name

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        validate_description(description)

        return description

    def clean_address(self):
        address = self.cleaned_data['address'].strip()
        validate_default(address)

        return address

    class Meta:
        model = Departament
        fields = ['name', 'address', 'establishment', 'description']
