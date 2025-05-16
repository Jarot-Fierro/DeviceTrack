from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import FormMixin, ProcessFormView
from django.forms.models import model_to_dict
from django.contrib import messages

from .forms import FormSubCategory
from .models import SubCategory, SubCategoryHistory


def save_history(request, instance, old_instance, action):
    model_name = instance.__class__.__name__

    from django.forms.models import model_to_dict

    if old_instance:
        old_data = model_to_dict(old_instance)
        old_data['id_subcategory'] = str(old_instance.id_subcategory)
        old_data['category'] = {
            'id': str(old_instance.category.id_category),
            'name': old_instance.category.name,
            'status': old_instance.category.status
        }
    else:
        old_data = None

    new_data = model_to_dict(instance)
    new_data['id_subcategory'] = str(instance.id_subcategory)
    new_data['category'] = {
        'id': str(instance.category.id_category),
        'name': instance.category.name,
        'status': instance.category.status
    }
    new_data['status'] = instance.status

    data = {
        'id_subcategory': str(instance.id_subcategory),
        'operation': action,
        'old_data': old_data,
        'new_data': new_data,
        'user_login_history': request.user.username if request.user.is_authenticated else 'anonymous',
        'user_login': request.user if request.user.is_authenticated else None
    }

    if model_name == 'SubCategory':
        SubCategoryHistory.objects.create(**data)


class BaseSubCategoryFormView(TemplateView, FormMixin):
    form_class = FormSubCategory
    template_name = 'subcategory_list.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object') and self.object:
            kwargs.update({'instance': self.object})

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = SubCategory.objects.all().filter(status='ACTIVE').order_by('-updated_at')
        context['object_list_inactive'] = SubCategory.objects.all().filter(status='INACTIVE').order_by('-updated_at')

        return context


class SubCategoryCreateView(BaseSubCategoryFormView, ProcessFormView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            messages.success(request, 'El registro a sido creado correctamente')
            save_history(request, form.instance, None, 'create')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return redirect('subcategory_list')


class SubCategoryUpdateView(BaseSubCategoryFormView, ProcessFormView):
    def get_object(self):
        return SubCategory.objects.get(pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()

        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        old_instance = SubCategory.objects.get(pk=form.instance.id_subcategory)

        if form.is_valid():
            if form.has_changed():
                messages.success(request, 'El registro fue actualizado correctamente')
                save_history(request, form.instance, old_instance, 'update')

                return self.form_valid(form)

            else:
                messages.info(request, 'No hubo cambios en el registro')
                return redirect('subcategory_list')
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_subcategory'] = self.get_object().id_subcategory

        return context

    def form_valid(self, form):
        form.save()
        return redirect('subcategory_list')


class SubCategoryToggleStatusView(View):
    def get(self, request, pk):
        instance = get_object_or_404(SubCategory, pk=pk)
        old_instance = SubCategory.objects.get(pk=pk)
        instance.status = 'INACTIVE' if instance.status == 'ACTIVE' else 'ACTIVE'
        instance.save(update_fields=['status', 'updated_at'])

        save_history(request, instance, old_instance, 'toggle')

        messages.success(request, 'El estado del registro fue actualizado correctamente')

        return redirect('subcategory_list')


class SubCategoryHistoryView(ListView):
    model = SubCategoryHistory
    template_name = 'subcategory_list_history.html'

    def get_queryset(self):
        return SubCategoryHistory.objects.all().order_by('-updated_at')

