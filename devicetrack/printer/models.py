import uuid

from django.contrib.auth.models import User
from django.db import models

from brand.models import Brand
from device_owner.models import DeviceOwner
from devicetrack.abstract import StandardModel
from inks.models import Inks
from model.models import Model
from subcategory.models import SubCategory


class Printer(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]
    STATUS_DEVICE = [
        ('ASSIGNED', 'ASIGNADO'),
        ('IN_STOCK', 'EN BODEGA'),
    ]

    id_printer = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    number_serie = models.CharField(max_length=100)
    hh = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=150, choices=STATUS, default='ACTIVE')
    status_device = models.CharField(max_length=150, choices=STATUS_DEVICE, default='IN_STOCK')

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    inks = models.ForeignKey(Inks, on_delete=models.CASCADE)
    device_owner = models.ForeignKey(DeviceOwner, on_delete=models.CASCADE)

    @property
    def universal_id(self):
        return self.id_printer
    
    def __str__(self):
        return self.number_serie


class PrinterHistory(StandardModel):
    id_printer_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_printer = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_printer
