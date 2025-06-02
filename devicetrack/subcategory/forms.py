from django import forms
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

    class Meta:
        model = SubCategory
        fields = ['name', 'category']
