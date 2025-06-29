import uuid

from django.contrib.auth.models import User
from django.db import models

from devicetrack.abstract import StandardModel
from establishment.models import Establishment


class Departament(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]

    id_departament = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=150, choices=STATUS, default='ACTIVE')

    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class DepartamentHistory(StandardModel):
    id_departament_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_departament = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_departament
