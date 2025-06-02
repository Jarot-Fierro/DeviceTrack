from django.forms.models import model_to_dict
from datetime import datetime, date
from uuid import UUID

from brand.models import BrandHistory
from category.models import CategoryHistory
from chip.models import ChipHistory
from company.models import CompanyHistory
from device_owner.models import DeviceOwnerHistory
from leadership.models import LeadershipHistory
from model.models import ModelHistory
from operative_system.models import OperativeSystemHistory
from plan.models import PlanHistory
from subcategory.models import SubCategoryHistory
from typeplan.models import TypePlanHistory


def extended_model_to_dict(instance, fields=None, exclude=None):
    data = model_to_dict(instance, fields=fields, exclude=exclude)

    for key, value in data.items():
        if hasattr(value, 'all'):  # ManyToMany
            data[key] = list(value.values_list('pk', flat=True))
        elif hasattr(value, 'pk'):  # ForeignKey
            data[key] = value.pk
        elif isinstance(value, (datetime, date)):
            data[key] = value.isoformat()  # Format ISO 8601: "YYYY-MM-DD"
        elif isinstance(value, UUID):  # UUID
            data[key] = str(value)
        elif isinstance(value, bytes):  # Bytes
            data[key] = str(value)

    return data


def save_history_standard(request, instance, action):
    model_name = instance.__class__.__name__

    print(model_name)

    # Search "id_" in the model
    id_field = next((field.name for field in instance._meta.fields if field.name.startswith('id_')), None)

    if not id_field:
        raise Exception(f"No se encontró campo que comience con 'id_' en el modelo {model_name}")

    # id_name = f'id_{id_field}'.lower()
    #
    print(id_field)

    data = {
        id_field: str(getattr(instance, id_field)),
        'operation': action,
        'data': extended_model_to_dict(instance),
        'user_login_history': request.user.username if request.user.username else 'anonymous',
        'user_login_id': request.user.id if request.user.is_authenticated else None
    }

    match model_name:
        case 'Brand':
            BrandHistory.objects.create(**data)

        case 'Category':
            CategoryHistory.objects.create(**data)

        case 'SubCategory':
            SubCategoryHistory.objects.create(**data)

        case 'Model':
            ModelHistory.objects.create(**data)

        case 'Leadership':
            LeadershipHistory.objects.create(**data)

        case 'OperativeSystem':
            OperativeSystemHistory.objects.create(**data)

        case 'DeviceOwner':
            DeviceOwnerHistory.objects.create(**data)

        case 'Company':
            CompanyHistory.objects.create(**data)

        case 'TypePlan':
            TypePlanHistory.objects.create(**data)

        case 'Plan':
            PlanHistory.objects.create(**data)

        case 'Chip':
            ChipHistory.objects.create(**data)

