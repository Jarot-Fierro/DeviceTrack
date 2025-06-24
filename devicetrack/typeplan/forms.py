from django import forms
from django.core.validators import MaxLengthValidator

from devicetrack.validation_forms import validate_name, validate_description
from .models import TypePlan


class FormTypePlan(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_type_plan',
                'class': 'form-control',
                'placeholder': 'Nombre del Plan',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'description_type_plan',
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

        exists = TypePlan.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(name, exists)

        return name

    def clean_description(self):
        description = self.cleaned_data['description'].strip()

        validate_description(description)

        return description

    class Meta:
        model = TypePlan
        fields = ['name', 'description']
