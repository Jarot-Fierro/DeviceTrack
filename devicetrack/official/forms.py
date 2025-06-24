from django import forms

from departament.models import Departament
from devicetrack.validation_forms import (
    validate_rut,
    validate_default,
    validate_name,
    validate_email
)
from .models import Official


class FormOfficial(forms.ModelForm):
    first_names = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'first_names_official',
                'class': 'form-control',
                'placeholder': 'Nombres',
                'min-lenght': 1,
                'max-lenght': 150
            }),
        required=True
    )
    pather_surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'pather_surname_official',
                'class': 'form-control',
                'placeholder': 'Apellido Paterno',
                'min-lenght': 1,
                'max-lenght': 150
            }),
        required=True
    )
    mather_surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'mather_surname_official',
                'class': 'form-control',
                'placeholder': 'Apellido Materno',
                'min-lenght': 1,
                'max-lenght': 150
            }),
        required=True
    )
    rut = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'rut_official',
                'class': 'form-control',
                'placeholder': '12345678-9',
                'min-lenght': 1,
                'max-lenght': 150
            }),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'id': 'email_official',
                'class': 'form-control',
                'placeholder': 'ejemplo@gmail.com',
                'min-lenght': 1,
                'max-lenght': 150
            }),
        required=True
    )
    departament = forms.ModelChoiceField(
        queryset=Departament.objects.all().filter(status='ACTIVE'),
        empty_label="Seleccione un departamento",
        widget=forms.Select(
            attrs={
                'id': 'departament_official',
                'class': 'form-control',
            }
        ),
        required=False
    )

    def clean_first_names(self):
        first_names = self.cleaned_data['first_names'].strip()
        validate_default(first_names)

        return first_names

    def clean_pather_surname(self):
        pather_surname = self.cleaned_data['pather_surname'].strip()
        validate_default(pather_surname)

        return pather_surname

    def clean_mather_surname(self):
        mather_surname = self.cleaned_data['mather_surname'].strip()
        validate_default(mather_surname)

        return mather_surname

    def clean_rut(self):
        rut = self.cleaned_data['rut'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Official.objects.filter(rut__iexact=rut).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(rut, exists, 'RUT')

        validate_rut(rut)

        return rut

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Official.objects.filter(email__iexact=email).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(email, exists, 'correo electrónico')
        validate_email(email)

        return email

    class Meta:
        model = Official
        fields = ['first_names', 'pather_surname', 'mather_surname', 'rut', 'email', 'departament']
