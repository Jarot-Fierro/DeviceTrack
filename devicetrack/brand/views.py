from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView, View
from django.forms.models import model_to_dict
from django.contrib import messages

from .models import Brand, BrandHistory
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
        context['object_list'] = Brand.objects.all().filter(status='ACTIVE').order_by('-updated_at')
        context['object_list_inactive'] = Brand.objects.all().filter(status='INACTIVE').order_by('-updated_at')

        return context

    def save_history(self, instance, action):
        request = self.request

        data = model_to_dict(instance)  # Toda la instancia actual

        if action == 'Create':
            BrandHistory.objects.create(
                id_brand=instance.id_brand,
                operation=action,
                old_data=None,
                new_data=data,
                user_login_history=request.user.username,
                user_login=request.user
            )
        # elif action == 'update':
        #     old_instance = Brand.objects.get(pk=instance.pk)
        #     old_data = model_to_dict(old_instance)
        #     new_data = data
        #
        #     # Solo guardamos los campos que cambiaron
        #     changed_data = {
        #         field: new_data[field]
        #         for field in new_data
        #         if old_data.get(field) != new_data[field]
        #     }
        #
        #     if changed_data:
        #         BrandHistory.objects.create(
        #             brand=instance,
        #             operation=action,
        #             old_data=old_data,
        #             new_data=changed_data,
        #             user_login_history=request.user if request.user.is_authenticated else None
        #         )
        # elif action == 'toggle':
        #     old_status = getattr(instance, 'status', '')
        #     new_status = 'INACTIVE' if old_status == 'ACTIVE' else 'ACTIVE'
        #
        #     BrandHistory.objects.create(
        #         brand=instance,
        #         operation=action,
        #         old_data={'status': old_status},
        #         new_data={'status': new_status},
        #         user_login_history=request.user if request.user.is_authenticated else None
        #     )


class BrandCreateView(BaseBrandFormView, ProcessFormView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'El registro a sido creado correctamente')
            self.save_history(form.instance, 'create')
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
                self.save_history(form.instance, 'update')
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


class BrandHistoryView(ListView):
    model = BrandHistory
    template_name = 'brand_list_history.html'
