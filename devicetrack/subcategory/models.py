from django.db import models
from devicetrack.abstract import StandardModel
from django.contrib.auth.models import User
from category.models import Category
import uuid


class SubCategory(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE')
    ]

    id_subcategory = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS, default='ACTIVE')

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubCategoryHistory(StandardModel):
    id_subcategory_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_subcategory = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_subcategory
