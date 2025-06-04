import uuid

from django.contrib.auth.models import User
from django.db import models

from brand.models import Brand
from chip.models import Chip
from devicetrack.abstract import StandardModel
from model.models import Model
from subcategory.models import SubCategory


class Phone(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]

    id_phone = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    imei = models.CharField(max_length=30)
    status = models.CharField(max_length=150, choices=STATUS, default='ACTIVE')

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    chip = models.ForeignKey(Chip, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    models = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self):
        return self.imei


class PhoneHistory(StandardModel):
    id_phone_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_phone = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_phone
