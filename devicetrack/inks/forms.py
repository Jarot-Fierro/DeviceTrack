from django import forms

from devicetrack.validation_forms import validate_name
from .models import Inks


class FormInks(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_inks',
                'class': 'form-control',
                'placeholder': 'Tinta',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        current_instance = self.instance if self.instance.pk else None

        exists = Inks.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(name, exists, 'nombre')

        return name

    class Meta:
        model = Inks
        fields = ['name']
