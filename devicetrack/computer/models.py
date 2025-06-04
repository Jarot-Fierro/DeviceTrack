import uuid

from django.contrib.auth.models import User
from django.db import models

from brand.models import Brand
from device_owner.models import DeviceOwner
from devicetrack.abstract import StandardModel
from licence_os.models import LicenceOs
from microsoft_office.models import MicrosoftOffice
from model.models import Model
from subcategory.models import SubCategory


class Computer(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]

    id_computer = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    number_serie = models.CharField(max_length=100)
    mac = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=150, choices=STATUS, default='ACTIVE')

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    licence_os = models.ForeignKey(LicenceOs, on_delete=models.CASCADE)
    microsoft_office = models.ForeignKey(MicrosoftOffice, on_delete=models.CASCADE)
    device_owner = models.ForeignKey(DeviceOwner, on_delete=models.CASCADE)

    def __str__(self):
        return self.number_serie


class ComputerHistory(StandardModel):
    id_computer_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_computer = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_computer
