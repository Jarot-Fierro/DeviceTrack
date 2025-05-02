from django.shortcuts import render


def brand_list(request):
    return render(request, 'brand_list.html')
