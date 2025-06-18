from django.http import JsonResponse

from article.models import Article
from computer.models import Computer
from phone.models import Phone
from printer.models import Printer


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
        device = Model.objects.get(pk=device_id)
        official = getattr(device, 'official', None) or getattr(device, 'device_owner', None)
        name = str(official) if official else "No asignado"
        return JsonResponse({'official_name': name})
    except Model.DoesNotExist:
        return JsonResponse({'error': 'No encontrado'}, status=404)
