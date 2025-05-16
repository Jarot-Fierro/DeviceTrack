from django.db import models
from devicetrack.abstract import StandardModel
from django.contrib.auth.models import User
import uuid


class Category(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE')
    ]

    id_category = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS, default='ACTIVE')

    def __str__(self):
        return self.name


class CategoryHistory(StandardModel):
    id_category_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_category = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    new_data = models.JSONField()
    old_data = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_category
