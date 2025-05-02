from devicetrack.abstract import StandardModel
from django.db import models
import uuid


class Brand(StandardModel):
    STATUS = [
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
        ('DELETED', 'DELETED'),
    ]

    id_brand = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=150, choices=STATUS)

    def __str__(self):
        return self.name
