from datetime import datetime, date
from uuid import UUID

from django.forms.models import model_to_dict

from brand.models import BrandHistory
from category.models import CategoryHistory
from chip.models import ChipHistory
from company.models import CompanyHistory
from computer.models import ComputerHistory
from device_owner.models import DeviceOwnerHistory
from leadership.models import LeadershipHistory
from licence_os.models import LicenceOsHistory
from microsoft_office.models import MicrosoftOfficeHistory
from model.models import ModelHistory
from operative_system.models import OperativeSystemHistory
from phone.models import PhoneHistory
from plan.models import PlanHistory
from subcategory.models import SubCategoryHistory
from typeplan.models import TypePlanHistory


def rut_validate(rut: str) -> bool:
    rut = rut.replace(".", "").replace("-", "").upper()
    if not rut or len(rut) < 2:
        return False

    body = rut[:-1]
    dv = rut[-1]

    try:
        body_num = int(body)
    except ValueError:
        return False

    sum = 0
    multi = 2
    for i in reversed(str(body_num)):
        sum += int(i) * multi
        multi = 2 if multi == 7 else multi + 1

    response = 11 - (sum % 11)
    if response == 11:
        dv_response = '0'
    elif response == 10:
        dv_response = 'K'
    else:
        dv_response = str(response)

    return dv == dv_response


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

        case 'Phone':
            PhoneHistory.objects.create(**data)

        case 'LicenceOs':
            LicenceOsHistory.objects.create(**data)

        case 'MicrosoftOffice':
            MicrosoftOfficeHistory.objects.create(**data)

        case 'Computer':
            ComputerHistory.objects.create(**data)
