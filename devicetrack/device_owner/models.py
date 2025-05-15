from devicetrack.abstract import StandardModel
from django.db import models
from django.contrib.auth.models import User
import uuid


class DeviceOwner(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]

    id_device_owner = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    status = models.CharField(max_length=150, choices=STATUS, default='ACTIVE')

    def __str__(self):
        return self.name


class DeviceOwnerHistory(StandardModel):
    id_device_owner_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_device_owner = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    new_data = models.JSONField()
    old_data = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_device_owner

