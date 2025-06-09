import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from brand.models import Brand
from devicetrack.abstract import StandardModel
from model.models import Model

STATUS = [
    ('ACTIVE', 'ACTIVE'),
    ('INACTIVE', 'INACTIVE'),
]

SERIAL_STATUS = [
    ('AVAILABLE', _('Disponible')),
    ('IN_USE', _('En uso')),
    ('UNAVAILABLE', _('No disponible')),
    ('IN_REPAIR', _('En reparación')),
    ('DAMAGED', _('Dañado')),
    ('LOST', _('Perdido')),
    ('DECOMMISSIONED', _('Dado de baja')),
    ('RESERVED', _('Reservado')),
    ('RETURNED', _('Devuelto')),
    ('STOLEN', _('Robado')),
    ('DEFECTIVE', _('Defectuoso')),
    ('UNDER_TESTING', _('En pruebas')),
    ('CALIBRATION', _('En calibración')),
]


# Base Model
class Article(StandardModel):
    id_article = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS, default='ACTIVE')

    description = models.TextField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, blank=True)
    is_serialized = models.BooleanField(default=False)  # Indicates if the article has serial numbers

    def __str__(self):
        return self.name


# Modelo for Stock of the Article Generic
class ArticleStock(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, primary_key=True, related_name='stock_obj')
    stock = models.PositiveIntegerField(default=0)  # Total Stock

    def __str__(self):
        return f"{self.article.name} - Stock: {self.stock}"


# Modelo for Serial Numbers of the Article
class SerialNumber(StandardModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='serials')
    serial_code = models.CharField(max_length=100, unique=True)
    serial_status = models.CharField(max_length=20, choices=SERIAL_STATUS, default='AVAILABLE')

    def __str__(self):
        return f"{self.article.name} - SN: {self.serial_code}"


class ArticleHistory(StandardModel):
    id_article_history = models.AutoField(primary_key=True, unique=True, editable=False)
    id_article = models.CharField(max_length=200)
    operation = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_login_history = models.CharField(max_length=100)

    # Foreignkey
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id_article
