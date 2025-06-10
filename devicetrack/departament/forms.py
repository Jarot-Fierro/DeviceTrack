from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from establishment.models import Establishment
from .models import Departament

STATUS = [
    ('ACTIVE', 'Activo'),
    ('INACTIVE', 'Inactivo'),
]


class FormDepartament(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_departament',
                'class': 'form-control',
                'placeholder': 'Nombre del Departamento',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'address_departament',
                'class': 'form-control',
                'placeholder': 'Calle y número',
                'min-lenght': 1,
                'max-lenght': 100
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

        if exists:
            raise ValidationError("Ya existe una marca con este nombre.")

        return name

    class Meta:
        model = Departament
        fields = ['name', 'address', 'establishment', 'description']
