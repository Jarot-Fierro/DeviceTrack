from django import forms
from django.core.exceptions import ValidationError
from .models import Chip
from company.models import Company
from plan.models import Plan


STATUS = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]


class FormChip(forms.ModelForm):
    number_phone = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'id': 'number_phone_brand',
                'class': 'form-control',
                'placeholder': '12345678',
                'minlength': '8',
                'maxlength': '8',
            }),
        required=True
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

    class Meta:
        model = Chip
        fields = ['number_phone', 'company', 'plan']
