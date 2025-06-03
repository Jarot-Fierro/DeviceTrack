import uuid

from django.contrib.auth.models import User
from django.db import models

from devicetrack.abstract import StandardModel


class Official(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]

    id_official = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    first_names = models.CharField(max_length=200)
    pather_surname = models.CharField(max_length=200)
    mather_surname = models.CharField(max_length=200, null=True, blank=True)
    rut = models.CharField(max_length=10)
    email = models.CharField(max_length=200)
    status = models.CharField(max_length=150, choices=STATUS, default='ACTIVE')

    # Foreignkey
    #     departament = models.ForeignKey(Departament, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_names} {self.pather_surname}"


class OfficialHistory(StandardModel):
    id_official_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_official = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_official
