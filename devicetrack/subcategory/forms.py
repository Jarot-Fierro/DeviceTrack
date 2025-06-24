from django import forms

from devicetrack.validation_forms import validate_name
from .models import SubCategory, Category


class FormSubCategory(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_category',
                'class': 'form-control',
                'placeholder': 'Nombre de la Subcategoría',
                'min-lenght': 1,
                'max-lenght': 100
            }
        ),
        required=True
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(status='ACTIVE'),
        empty_label="--  Selecciona una opción  --",
        widget=forms.Select(
            attrs={
                'id': 'category_select',
                'class': 'form-control'
            }
        ),
        required=True
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        current_instance = self.instance if self.instance.pk else None
        exists = SubCategory.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(name, exists, 'Nombre')

        return name

    class Meta:
        model = SubCategory
        fields = ['name', 'category']
