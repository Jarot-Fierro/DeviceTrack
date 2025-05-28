from devicetrack.abstract import StandardModel
from django.db import models
from django.contrib.auth.models import User
from plan.models import Plan
from company.models import Company
import uuid


class Chip(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]

    id_chip = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    number_phone = models.PositiveIntegerField()
    status = models.CharField(max_length=150, choices=STATUS, default='ACTIVE')

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.number_phone}"


class ChipHistory(StandardModel):
    id_chip_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_chip = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id_chip_history}"
