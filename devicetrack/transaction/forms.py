from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from official.models import Official
from soporte.models import Soporte
from .models import TransactionOutput


class EntryForm(forms.Form):
    device = forms.ModelChoiceField(
        empty_label="Seleccione un equipo",
        queryset=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
    )
    official = forms.ModelChoiceField(
        queryset=Official.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )
    observation = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'transaction_observation',
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe más detalles aquí...'
            }),
        required=False,
        validators=[MaxLengthValidator(200, message='No puedes escribir más de 200 caracteres.')],
    )

    def clean(self):
        cleaned_data = super().clean()
        official = cleaned_data.get('official')

        if not official:
            raise forms.ValidationError("No se pudo obtener el funcionario asociado al dispositivo.")

        return cleaned_data


class OutputForm(forms.Form):
    device = forms.ModelChoiceField(
        empty_label="Seleccione un equipo",
        queryset=None,  # Se asigna dinámicamente desde la vista
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    official = forms.ModelChoiceField(
        queryset=Official.objects.filter(status='ACTIVE'),
        empty_label="Seleccione un funcionario",
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    type_output = forms.ChoiceField(
        choices=TransactionOutput.OUTPUT_TYPES,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    return_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        type_output = cleaned_data.get('type_output')
        return_date = cleaned_data.get('return_date')

        if type_output == 'LOAN' and not return_date:
            raise ValidationError("Debe especificar la fecha de devolución para préstamos.")

        return cleaned_data


class SupportForm(forms.Form):
    device = forms.ModelChoiceField(
        queryset=None,
        empty_label="Seleccione un equipo",
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    official = forms.ModelChoiceField(
        queryset=Official.objects.filter(status='ACTIVE'),
        empty_label="Seleccione un funcionario",
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    type_soporte = forms.ModelChoiceField(
        queryset=Soporte.objects.filter(status='ACTIVE'),
        empty_label="Seleccione un soporte",
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    date_start = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )

    date_end = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )

    problem = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe el problema'}
        ),
        validators=[MaxLengthValidator(200)],
    )

    solution = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe la solución si aplica'}
        ),
        validators=[MaxLengthValidator(200)],
    )
