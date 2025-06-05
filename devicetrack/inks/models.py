import uuid

from django.contrib.auth.models import User
from django.db import models

from devicetrack.abstract import StandardModel


class Inks(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]

    id_inks = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=150, choices=STATUS, default='ACTIVE')

    def __str__(self):
        return self.name


class InksHistory(StandardModel):
    id_inks_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_inks = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_inks
