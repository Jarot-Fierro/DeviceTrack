from django import forms
from django.core.exceptions import ValidationError
from .models import Model


STATUS = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]


class FormModel(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_model',
                'class': 'form-control',
                'placeholder': 'Nombre del modelo',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Model.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        if exists:
            raise ValidationError("Ya existe un modelo con este nombre.")

        return name

    class Meta:
        model = Model
        fields = ['name']
