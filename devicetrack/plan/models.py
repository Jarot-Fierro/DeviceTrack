from devicetrack.abstract import StandardModel
from django.db import models
from django.contrib.auth.models import User
from typeplan.models import TypePlan
from django.utils import timezone
import uuid


class Plan(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    ]
    STATUS_BILLING = [
        ('PENDING', 'PENDING'),
        ('PAYING', 'PAYING'),
        ('CANCELED', 'CANCELED'),
    ]

    id_plan = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)

    gigabytes = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0)
    messages = models.PositiveIntegerField(default=0)

    unlimited_gigabytes = models.BooleanField(default=False)
    unlimited_minutes = models.BooleanField(default=False)
    unlimited_messages = models.BooleanField(default=False)

    price = models.PositiveIntegerField(default=0)

    status_billing = models.CharField(max_length=150, choices=STATUS_BILLING, default='PENDING')

    status = models.CharField(max_length=150, choices=STATUS, default='ACTIVE')
    date_hiring = models.DateField(default=timezone.now, null=True, blank=True)
    date_cancellation = models.DateField(null=True, blank=True)
    reason_cancellation = models.CharField(max_length=200, null=True, blank=True)

    type_plan = models.ForeignKey(TypePlan, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.unlimited_gigabytes:
            self.gigabytes = 0
        if self.unlimited_minutes:
            self.minutes = 0
        if self.unlimited_messages:
            self.messages = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PlanHistory(StandardModel):
    id_plan_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_plan = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type_plan = models.ForeignKey(TypePlan, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_plan

