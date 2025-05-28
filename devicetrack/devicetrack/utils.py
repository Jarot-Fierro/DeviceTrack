from django.forms.models import model_to_dict
from datetime import datetime
from uuid import UUID
from chip.models import ChipHistory


def extended_model_to_dict(instance, fields=None, exclude=None):
    data = model_to_dict(instance, fields=fields, exclude=exclude)

    for key, value in data.items():
        if hasattr(value, 'all'):  # ManyToMany
            data[key] = list(value.values_list('pk', flat=True))
        elif hasattr(value, 'pk'):  # ForeignKey
            data[key] = value.pk
        elif isinstance(value, (datetime, UUID)):  # UUID y datetime
            data[key] = str(value)
        elif isinstance(value, bytes):  # Bytes
            data[key] = str(value)

    return data


def save_history_standard(request, instance, action):
    model_name = instance.__class__.__name__

    # Search "id_" in the model
    id_field = next((field.name for field in instance._meta.fields if field.name.startswith('id_')), None)

    if not id_field:
        raise Exception(f"No se encontró campo que comience con 'id_' en el modelo {model_name}")

    id_name = f'id_{model_name}'.lower()

    data = {
        id_name: str(getattr(instance, id_field)),
        'operation': action,
        'data': extended_model_to_dict(instance),
        'user_login_history': request.user.username if request.user.username else 'anonymous',
        'user_login_id': request.user.id if request.user.is_authenticated else None
    }

    match model_name:
        case 'Chip':
            ChipHistory.objects.create(**data)
