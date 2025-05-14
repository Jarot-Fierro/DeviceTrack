from django import forms
from django.core.exceptions import ValidationError
from .models import Leadership
from .utils import rut_validate


STATUS = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]


class FormLeadership(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_leadership',
                'class': 'form-control',
                'placeholder': 'Nombres y Apellidos',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    rut = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'rut_leadership',
                'class': 'form-control',
                'placeholder': '12345678-9',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'id': 'email_leadership',
                'class': 'form-control',
                'placeholder': 'ejemplo@gmail.com',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    boss_position = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'boss_position_leadership',
                'class': 'form-control',
                'placeholder': 'Cargo',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Leadership.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        if exists:
            raise ValidationError("Ya existe un registro con este nombre.")

        return name

    def clean_rut(self):
        rut = self.cleaned_data['rut'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Leadership.objects.filter(rut__iexact=rut).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        if exists:
            raise ValidationError("Ya existe un registro con este RUT.")

        if not rut_validate(rut):
            raise ValidationError("El RUT ingresado no es válido.")

        return rut

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Leadership.objects.filter(email__iexact=email).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        if exists:
            raise ValidationError("Ya existe un registro con este correo.")

        return email

    class Meta:
        model = Leadership
        fields = ['name', 'rut', 'email', 'boss_position']
