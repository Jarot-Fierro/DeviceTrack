# user/forms.py
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class CustomLoginForm(forms.Form):
    identifier = forms.CharField(
        label="Usuario o Correo",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Usuario o correo'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        password = cleaned_data.get('password')

        if identifier and password:
            # Intentar autenticar por username
            user = authenticate(username=identifier, password=password)

            if not user:
                # Buscar por correo
                try:
                    user_obj = User.objects.get(email=identifier)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if not user:
                raise forms.ValidationError("Credenciales inválidas.")

            self.user = user  # Guarda el usuario autenticado
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
