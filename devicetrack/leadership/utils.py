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
