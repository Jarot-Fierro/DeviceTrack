from django import forms
from django.core.exceptions import ValidationError

from company.models import Company
from plan.models import Plan
from .models import Chip


class FormChip(forms.ModelForm):
    number_phone = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'id': 'number_phone_brand',
                'class': 'form-control',
                'placeholder': '12345678',
                'min': '10000000',
                'max': '99999999',
            }),
        required=True,
        error_messages={
            'min_value': 'El valor debe ser mayor a 0',
            'invalid': 'El valor debe ser numérico'
        }
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.filter(status='ACTIVE'),
        empty_label='Selecciona la Compañía',
        widget=forms.Select(
            attrs={
                'id': 'company_chip',
                'class': 'form-control'
            }),
        required=True
    )
    plan = forms.ModelChoiceField(
        queryset=Plan.objects.filter(status='ACTIVE'),
        empty_label='Selecciona el Plan',
        widget=forms.Select(
            attrs={
                'id': 'plan_chip',
                'class': 'form-control'
            }
        )
    )

    def clean_number_phone(self):
        number = self.cleaned_data['number_phone']
        if not (10000000 <= number <= 99999999):
            raise ValidationError("El número debe tener exactamente 8 dígitos.")
        return number

    class Meta:
        model = Chip
        fields = ['number_phone', 'company', 'plan']
