from django.contrib.auth.models import User
from django.db import models

ROL = [
    ('soporte', 'Soporte'),
    ('administrador', 'Administrador')
]


class PerfilUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photo_user/', blank=True, null=True)
    signature = models.ImageField(upload_to='signal_user/', blank=True, null=True)
    rol = models.CharField(max_length=50, choices=ROL, default='Soporte')
    activo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
