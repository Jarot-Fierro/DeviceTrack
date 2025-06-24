from django import forms
from django.core.validators import MaxLengthValidator

from devicetrack.validation_forms import validate_name, validate_description
from .models import Establishment


class FormEstablishment(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_establishment',
                'class': 'form-control',
                'placeholder': 'Nombre del Establecimiento',
                'minlenght': '1',
                'maxlenght': '100'
            }),
        required=True
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'city_establishment',
                'class': 'form-control',
                'placeholder': 'Santiago',
                'minlenght': '1',
                'maxlenght': '100'
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

        exists = Establishment.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(name, exists, 'nombre del establecimiento')

        return name

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        validate_description(description)

        return description

    class Meta:
        model = Establishment
        fields = ['name', 'city', 'description']
