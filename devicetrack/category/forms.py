from django import forms

from devicetrack.validation_forms import validate_name
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
        ),
        required=True
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        current_instance = self.instance if self.instance.pk else None
        exists = Category.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(name, exists, 'Nombre')

        return name

    class Meta:
        model = Category
        fields = ['name']
