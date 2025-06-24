from django import forms
from django.core.validators import MaxLengthValidator

from brand.models import Brand
from devicetrack.validation_forms import validate_name, validate_description
from model.models import Model
from .models import SerialNumber, Article


class FormArticle(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'name_article',
                'class': 'form-control',
                'placeholder': 'Nombre del artículo',
                'min-lenght': 1,
                'max-lenght': 100
            }),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'id': 'description_device_owner',
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe más detalles aquí...'
            }),
        required=False,
        validators=[MaxLengthValidator(200, message='No puedes escribir más de 200 caracteres.')],
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'brand_article',
            }
        ),
        required=True
    )
    model = forms.ModelChoiceField(
        queryset=Model.objects.all().filter(status='ACTIVE'),
        empty_label='Selecciona una opción',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'model_article',
            }
        ),
        required=True
    )
    is_serialized = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'is_serialized_article'
            }
        ),
        required=False
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        current_instance = self.instance if self.instance.pk else None
        exists = Article.objects.filter(name__iexact=name).exclude(
            pk=current_instance.pk if current_instance else None).exists()

        validate_name(name, exists)

        return name

    def clean_description(self):
        description = self.cleaned_data['description'].strip()

        validate_description(description)

        return description

    class Meta:
        fields = [
            'name',
            'description',
            'brand',
            'model',
            'is_serialized',
        ]
        model = Article


class FormArticleUpdate(FormArticle):
    class Meta(FormArticle.Meta):
        exclude = ['is_serialized']


class FormStock(forms.Form):
    stock = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        error_messages={
            'min_value': 'El valor debe ser mayor a 0',
            'invalid': 'El valor debe ser numérico'
        }
    )


class FormSerialNumber(forms.ModelForm):
    def clean_serial_code(self):
        code = self.cleaned_data['serial_code']
        # Si es actualización, excluir la instancia actual
        qs = SerialNumber.objects.filter(serial_code=code)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Este código de serie ya existe.")
        return code

    class Meta:
        model = SerialNumber
        fields = ['serial_code', 'serial_status']
        widgets = {
            'serial_code': forms.TextInput(attrs={"class": "form-control"}),
            'serial_status': forms.Select(attrs={"class": "form-control"})
        }
