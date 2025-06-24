from django import forms
from django.core.exceptions import ValidationError

from brand.models import Brand
from chip.models import Chip
from model.models import Model
from subcategory.models import SubCategory
from .models import Phone


class FormPhone(forms.ModelForm):
    imei = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'imei_phone',
                'class': 'form-control',
                'placeholder': 'IMEI del teléfono',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'brand_phone',
            }
        ),
        required=True
    )
    models = forms.ModelChoiceField(
        queryset=Model.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'model_phone',
            }
        ),
        required=True
    )
    chip = forms.ModelChoiceField(
        queryset=Chip.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'chip_phone',
            }
        ),
        required=True
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'subcategory_phone',
            }
        ),
        required=True
    )

    def clean_imei(self):
        imei = self.cleaned_data['imei'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Phone.objects.filter(imei__iexact=imei).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        if exists:
            raise ValidationError("Ya existe una registro con este IMEI.")

        return imei

    class Meta:
        model = Phone
        fields = ['imei', 'brand', 'models', 'chip', 'subcategory']
