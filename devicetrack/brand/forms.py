from django import forms

from devicetrack.validation_forms import validate_name
from .models import Brand


class FormBrand(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_brand',
                'class': 'form-control',
                'placeholder': 'Nombre de la Marca',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Brand.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(name, exists, 'Nombre')
        return name

    class Meta:
        model = Brand
        fields = ['name']
