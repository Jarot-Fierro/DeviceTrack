from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from .models import OperativeSystem


STATUS = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]


class FormOperativeSystem(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_brand',
                'class': 'form-control',
                'placeholder': 'Nombre del Sistema Operativo',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'name_brand',
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

        exists = OperativeSystem.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        if exists:
            raise ValidationError("Ya existe una marca con este nombre.")

        return name

    class Meta:
        model = OperativeSystem
        fields = ['name', 'description']
