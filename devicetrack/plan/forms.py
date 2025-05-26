from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from .models import TypePlan, Plan


STATUS = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]

STATUS_BILLING = [
        ('PENDING', 'Pendiente'),
        ('PAYING', 'Pagando'),
        ('CANCELED', 'Cancelado'),
    ]


class FormPlan(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_plan',
                'class': 'form-control',
                'placeholder': 'Nombre del Plan',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    gigabytes = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'id': 'gigabytes_plan',
                'class': 'form-control'
            }),
        required=False
    )
    minutes = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'id': 'minutes_plan',
                'class': 'form-control'
            }),
        required=False
    )
    messages = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'id': 'messages_plan',
                'class': 'form-control'
            }),
        required=False
    )
    unlimited_gigabytes = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'id': 'unlimited_gigabytes_plan',
                'class': 'form-check-input'
            }),
        required=False
    )
    unlimited_minutes = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'id': 'unlimited_minutes_plan',
                'class': 'form-check-input'
            }),
        required=False
    )
    unlimited_messages = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'id': 'unlimited_messages_plan',
                'class': 'form-check-input'
            }),
        required=False
    )
    price = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'id': 'price_plan',
                'class': 'form-control'
            }),
        required=False
    )
    status_billing = forms.ChoiceField(
        choices=STATUS_BILLING,
        widget=forms.Select(
            attrs={
                'id': 'status_billing_plan',
                'class': 'form-control'
            }
        )
    )
    type_plan = forms.ModelChoiceField(
        queryset=TypePlan.objects.filter(status='ACTIVE'),
        empty_label="--  Selecciona el tipo de Plan  --",
        widget=forms.Select(
            attrs={
                'id': 'type_plan',
                'class': 'form-control'
            },
        ),
        required=True
    )

    date_hiring = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            },
            format='%Y-%m-%d'
        ),
        required=False
    )

    date_cancellation = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    reason_cancellation = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'reason_cancellation_plan',
                'class': 'form-control',
                'placeholder': 'Motivo de Cancelación',
                'max-lenght': 100
            }),
        required=False
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'description_plan',
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

        exists = Plan.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        if exists:
            raise ValidationError("Ya existe una marca con este nombre.")

        return name

    class Meta:
        model = Plan
        fields = [
            'name',
            'gigabytes',
            'minutes',
            'messages',
            'unlimited_gigabytes',
            'unlimited_minutes',
            'unlimited_messages',
            'price',
            'status_billing',
            'type_plan',
            'date_hiring',
            'date_cancellation'
        ]


class FormCancellationPlan(forms.ModelForm):
    date_cancellation = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            },
            format='%Y-%m-%d'
        ),
        required=True
    )
    reason_cancellation = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'reason_cancellation_plan',
                'class': 'form-control',
                'placeholder': 'Motivo de Cancelación',
                'max-lenght': 100
            }),
        required=True
    )

    class Meta:
        model = Plan
        fields = [
            'date_cancellation',
            'reason_cancellation',
        ]
