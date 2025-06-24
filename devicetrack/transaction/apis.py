from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from article.models import Article
from computer.models import Computer
from phone.models import Phone
from printer.models import Printer
from transaction.models import DetailTransaction


def get_official_for_device(request):
    device_type = request.GET.get('type')
    device_id = request.GET.get('device_id')

    model_map = {
        'phone': Phone,
        'computer': Computer,
        'printer': Printer,
        'article': Article,
    }

    Model = model_map.get(device_type)

    if not Model or not device_id:
        return JsonResponse({'error': 'Datos inválidos'}, status=400)

    try:
        # Obtener ContentType del modelo dinámico
        content_type = ContentType.objects.get_for_model(Model)

        # Buscar el último DetailTransaction con ese equipo
        last_detail = DetailTransaction.objects.filter(
            content_type=content_type,
            object_id=device_id
        ).order_by('-created_at').first()

        if not last_detail:
            return JsonResponse({'official_name': 'Sin historial'})

        # Obtener el oficial desde la transacción
        official = last_detail.transaction.official
        name = str(official) if official else "No asignado"

        return JsonResponse({'official_name': name})

    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)
