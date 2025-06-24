from django import forms
from django.core.validators import MaxLengthValidator

from devicetrack.validation_forms import validate_name, validate_description
from .models import MicrosoftOffice


class FormMicrosoftOffice(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_microsoft_office',
                'class': 'form-control',
                'placeholder': 'Nombre de la versión',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'description_microsoft_office',
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

        exists = MicrosoftOffice.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(name, exists, 'nombre')

        return name

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        validate_description(description)

        return description

    class Meta:
        model = MicrosoftOffice
        fields = ['name', 'description']
