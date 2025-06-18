from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from devicetrack.abstract import StandardModel


class Transaction(StandardModel):
    TRANSACTION_TYPES = [
        ('ENTRY', 'Entrada'),
        ('OUTPUT', 'Salida'),
        ('SUPPORT', 'Soporte'),
    ]

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True, editable=False)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    observation = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='PENDING')

    official = models.ForeignKey('official.Official', on_delete=models.PROTECT, related_name='official_transactions')
    login_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user_transactions')

    def save(self, *args, **kwargs):
        is_new = self._state.adding and not self.code
        super().save(*args, **kwargs)
        if is_new:
            self.code = f"TRX-{self.id:06d}"
            self.save()


class TransactionOutput(StandardModel):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    OUTPUT_TYPES = [
        ('DELIVERY', 'Entrega Permanente'),
        ('LOAN', 'Préstamo'),
    ]

    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='output_info')
    type_output = models.CharField(max_length=10, choices=OUTPUT_TYPES)
    return_date = models.DateField(null=True, blank=True)
    load_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='ACTIVE')

    def clean(self):
        if self.type_output == 'LOAN' and not self.return_date:
            raise ValidationError("Debe especificar la fecha de devolución para préstamos.")


class SupportTransaction(StandardModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('IN_PROCESS', 'En proceso'),
        ('COMPLETED', 'Completado'),
    ]

    id = models.AutoField(primary_key=True, unique=True, editable=False)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='support_info')
    type_soporte = models.ForeignKey('soporte.Soporte', on_delete=models.PROTECT)
    login_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    problem = models.TextField()
    solution = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # Relación al equipo (genérica)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    device = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Soporte {self.id} - {self.type_soporte.name}"


class DetailTransaction(StandardModel):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='details')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    device = GenericForeignKey('content_type', 'object_id')

    amount = models.PositiveIntegerField(default=1)

    def clean(self):
        if hasattr(self.device, 'number_serie') or hasattr(self.device, 'imei'):
            if self.amount != 1:
                raise ValidationError("Los equipos con número de serie solo deben tener cantidad 1.")
