import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email, validate_ipv4_address
from django.utils import timezone


def validate_ip(ip):
    try:
        validate_ipv4_address(ip)
    except ValidationError:
        raise ValidationError("La dirección IP no es válida. Debe tener el formato 192.168.0.1")
    return ip


def validate_default(value):
    if not re.fullmatch(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ0-9]+(-[A-Za-zÁÉÍÓÚÑáéíóúñ0-9]+)?$', value):
        raise ValidationError("Solo se permiten letras, números y un solo guion opcional (no al inicio ni final).")


def validate_date_today(date):
    if date and date < timezone.now().date():
        raise ValidationError("La fecha no puede ser anterior a hoy.")
    return date


def validate_date_start_end(start_date, end_date):
    if end_date and start_date and end_date <= start_date:
        raise ValidationError("La fecha debe ser posterior a la fecha de inicio.")
    return end_date


def validate_name(name, exists, field_name):
    if exists:
        raise ValidationError(f"Ya existe un registro con este {field_name}.")

    # No debe tener más de un espacio entre palabras
    if '  ' in name:
        raise ValidationError("Solo se permite un espacio entre palabras.")

    # Solo letra, números y espacios
    if not re.fullmatch(r'[A-Za-zÁÉÍÓÚÑáéíóúñ0-9]+( [A-Za-zÁÉÍÓÚÑáéíóúñ0-9]+)?', name):
        raise ValidationError("Solo se permiten letras y un solo espacio opcional entre palabras.")


def validate_description(description):
    if not description:
        return description

    if '  ' in description:
        raise ValidationError("Solo se permite un espacio entre palabras.")

    # Solo letra, números, exclamaciones, interrogación y espacios
    if not re.fullmatch(r'[A-Za-zÁÉÍÓÚÑáéíóúñ0-9¿?¡!\-.,]+( [A-Za-zÁÉÍÓÚÑáéíóúñ0-9¿?¡!\-.,]+)?', description):
        raise ValidationError(
            "Solo se permiten letras, números, signos (!¡¿?.,-), y un solo espacio opcional entre palabras.")


def validate_email(email):
    email = email.strip()
    try:
        django_validate_email(email)
    except ValidationError:
        raise ValidationError("El correo electrónico no es válido.")
    return email


def validate_rut(rut: str) -> bool:
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
