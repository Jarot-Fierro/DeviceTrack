from django.views.generic import ListView

from transaction.models import DetailTransaction


class CoreView(ListView):
    template_name = 'index.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = DetailTransaction.objects.all().order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Transacciones'
        return context
