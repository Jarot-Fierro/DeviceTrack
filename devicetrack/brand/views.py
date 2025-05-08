from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView, View
from django.contrib import messages

from .models import Brand
from .forms import FormBrand


class BaseBrandFormView(TemplateView, FormMixin):
    form_class = FormBrand
    template_name = 'brand_list.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object') and self.object:
            kwargs.update({'instance': self.object})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Brand.objects.all().order_by('-updated_at')

        return context


class BrandCreateView(BaseBrandFormView, ProcessFormView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'El registro a sido creado correctamente')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return redirect('brand_list')


class BrandUpdateView(BaseBrandFormView, ProcessFormView):

    def get_object(self):
        return Brand.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if form.has_changed():
                messages.success(request, 'El registro fue actualizado correctamente')
                return self.form_valid(form)
            else:
                messages.info(request, 'No hubo cambios en el registro')
                return redirect('brand_list')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_brand'] = self.get_object().id_brand
        return context

    def form_valid(self, form):
        form.save()
        return redirect('brand_list')


class BrandToggleStatusView(View):
    def get(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)
        brand.status = 'INACTIVE' if brand.status == 'ACTIVE' else 'ACTIVE'
        brand.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'El estado de la marca fue actualizada correctamente')
        return redirect('brand_list')
