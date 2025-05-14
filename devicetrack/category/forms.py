from django import forms
from .models import Category


class FormCategory(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_category',
                'class': 'form-control',
                'placeholder': 'Nombre de la Categoría',
                'min-lenght': 1,
                'max-lenght': 100
            }
        ),required=True
    )

    class Meta:
        model = Category
        fields = ['name']
