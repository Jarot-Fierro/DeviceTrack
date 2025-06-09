from django.contrib import messages
from django.db.models import F, Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin, ProcessFormView, FormView, UpdateView

from devicetrack.utils import save_history_standard
from .forms import FormArticle, FormStock, FormSerialNumber, FormArticleUpdate
from .models import Article, ArticleHistory, SerialNumber, SerialNumberHistory
from .models import ArticleStock


def save_history_serials(request, serial, operation):
    SerialNumberHistory.objects.create(
        serial_number=serial,
        operation=operation,
        data={
            'serial_number': str(serial.pk),  # 👈 aquí está la clave que falta
            'serial_code': serial.serial_code,
            'article_id': str(serial.article.pk),
            'article_name': serial.article.name,
            'status': getattr(serial, 'serial_status', 'N/A')
        },
        user_login=request.user,
        user_login_history=str(request.user.username)
    )


class ArticleCreateView(TemplateView, FormMixin, ProcessFormView):
    template_name = 'article_list.html'
    form_class = FormArticle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['object_list'] = Article.objects.filter().order_by('-id_article')
        articles = Article.objects.annotate(
            stock=F('stock_obj__stock'),
            total_serials=Count('serials')
        ).filter(status='ACTIVE').order_by('-id_article')
        context['object_list'] = articles
        return context

    def form_valid(self, form):
        self.object = form.save()
        save_history_standard(self.request, self.object, 'create')
        messages.success(self.request, 'Artículo creado correctamente.')

        if self.object.is_serialized:
            return redirect('article_add_serials', pk=self.object.pk)
        else:
            return redirect('article_add_stock', pk=self.object.pk)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error en el formulario.')
        return self.render_to_response(self.get_context_data(form=form))


class ArticleAddStockView(FormView):
    template_name = 'article_add_stock.html'
    form_class = FormStock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.annotate(
            stock=F('stock_obj__stock'),
            total_serials=Count('serials')
        ).filter(status='ACTIVE').order_by('-id_article')
        context['object_list'] = articles
        return context

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=kwargs['pk'])
        if self.article.is_serialized:
            messages.warning(request, "Este artículo se gestiona por series. Redirigiendo...")
            return redirect(reverse('article_add_serials', kwargs={'pk': self.article.pk}))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        stock_obj, created = ArticleStock.objects.get_or_create(article=self.article)
        stock_obj.stock += form.cleaned_data['stock']
        stock_obj.save()
        messages.success(self.request, 'Stock agregado correctamente.')
        return redirect('article_list')


class ArticleAddSerialsView(TemplateView):
    template_name = 'article_add_serials.html'

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=kwargs['pk'])

        if not self.article.is_serialized:
            messages.warning(request, "Este artículo se gestiona por unidades. Redirigiendo...")
            return redirect(reverse('article_add_stock', kwargs={'pk': self.article.pk}))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        context['form'] = FormSerialNumber()
        context['serials'] = self.article.serials.all()
        return context

    def post(self, request, *args, **kwargs):
        form = FormSerialNumber(request.POST)
        if form.is_valid():
            serial = form.save(commit=False)
            serial.article = self.article
            serial.save()
            save_history_serials(request, serial, 'create')
            messages.success(request, 'Código agregado correctamente.')
            return redirect('article_add_serials', pk=self.article.pk)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ArticleUpdateView(TemplateView, FormMixin, ProcessFormView):
    template_name = 'article_list.html'
    form_class = FormArticleUpdate

    def get_object(self):
        return Article.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            if form.has_changed():
                messages.success(request, 'El registro fue actualizado correctamente')
                save_history_standard(request, form.instance, 'update')
                return self.form_valid(form)
            else:
                messages.info(request, 'No hubo cambios en el registro')
                return redirect('article_list')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_article'] = self.get_object().id_article
        context['object_list'] = Article.objects.filter(status='ACTIVE').order_by('-id_article')
        return context

    def form_valid(self, form):
        form.save()
        return redirect('article_list')


class ArticleToggleStatusView(View):
    def get(self, request, pk):
        instance = get_object_or_404(Article, pk=pk)

        instance.status = 'INACTIVE' if instance.status == 'ACTIVE' else 'ACTIVE'
        instance.save(update_fields=['status', 'updated_at'])

        save_history_standard(request, instance, 'toggle')

        messages.success(request, 'El estado del registro fue actualizado correctamente')
        if instance.status == 'ACTIVE':
            return redirect('article_deleted_records')
        else:
            return redirect('article_list')


class ArticleDeletedRecordsView(ListView):
    model = Article
    template_name = 'article_list_deleted_records.html'

    def get_queryset(self):
        return Article.objects.all().filter(status='INACTIVE').order_by('-updated_at')


class SerialNumberUpdateView(UpdateView):
    model = SerialNumber
    form_class = FormSerialNumber
    template_name = 'article_add_serials.html'

    def get_success_url(self):
        return reverse_lazy('article_add_stock', kwargs={'pk': self.object.article.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.object.article
        context['serials'] = self.object.article.serials.all()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        save_history_serials(self.request, self.object, 'update')
        messages.success(self.request, "Código de serie actualizado correctamente.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar el código de serie.")
        return super().form_invalid(form)


class ArticleHistoryView(ListView):
    model = ArticleHistory
    template_name = 'article_list_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        enriched_entries = []

        for history in ArticleHistory.objects.all().order_by('-timestamp'):
            try:
                article = Article.objects.get(id_article=history.id_article)
            except Article.DoesNotExist:
                article = None

            stock = 0
            total_serials = 0

            if article:
                # Acceder correctamente usando related_name
                try:
                    stock = article.stock_obj.stock
                except ArticleStock.DoesNotExist:
                    stock = 0

                total_serials = article.serials.count()

            enriched_entries.append({
                'history': history,
                'article': article,
                'stock': stock,
                'total_serials': total_serials,
            })

        context['object_list'] = enriched_entries
        return context


class SerialNumberHistoryView(ListView):
    model = SerialNumberHistory
    template_name = 'serial_number_list_history.html'

    def get_queryset(self):
        return SerialNumberHistory.objects.all().order_by('-updated_at')
