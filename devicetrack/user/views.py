from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.messages import add_message, SUCCESS
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, CreateView

from user.forms import CustomLoginForm, FormUsuario
from user.models import PerfilUser


@method_decorator(sensitive_post_parameters('password'), name='dispatch')
@method_decorator(never_cache, name='dispatch')
class LoginViewCustom(FormView):
    template_name = 'auth/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('index')  # Cambia por la vista principal después de login
    redirect_authenticated_user = True  # lo mantendremos como propiedad manual

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return self.redirect_to_success_url()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Autenticar usuario y manejar sesión"""
        user = form.get_user()
        login(self.request, user)
        self.request.session.set_expiry(0)

        add_message(self.request, SUCCESS, 'Inicio de sesión exitoso.', extra_tags='auth_success')
        return super().form_valid(form)

    def redirect_to_success_url(self):
        return redirect(self.get_success_url())


@method_decorator(never_cache, name='dispatch')
class LogoutViewCustom(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        request.session.flush()
        add_message(self.request, SUCCESS, 'Se cerró la sesión correctamente.', extra_tags='auth_success')
        return response


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'user_profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        try:
            perfil = user.perfiluser
        except PerfilUser.DoesNotExist:
            perfil = None

        usuarios = User.objects.all().select_related('perfiluser')

        context = {
            'user': user,
            'perfil': perfil,
            'list_user': usuarios
        }
        return render(request, self.template_name, context)


class UserCreateView(CreateView):
    model = User
    form_class = FormUsuario
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_profile')
    success_message = "Usuario creado exitosamente."

    def form_valid(self, form):
        print("✅ form_valid ejecutado")
        user = form.save(commit=False)

        password = form.cleaned_data.get('password')
        if password:
            user.set_password(password)
            print("🔐 Contraseña seteada")

        user.save()
        print("👤 Usuario guardado:", user)

        PerfilUser.objects.get_or_create(user=user)
        messages.success(self.request, self.success_message)

        return super().form_valid(form)

    def form_invalid(self, form):
        print("❌ Formulario inválido")
        print(form.errors)
        return super().form_invalid(form)


class UserUpdateView(View):
    template_name = 'user_form.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = FormUsuario(instance=user)
        return render(request, self.template_name, {'form': form, 'id': pk})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = FormUsuario(request.POST, instance=user)

        if form.is_valid():
            user = form.save(commit=False)

            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)

            user.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('user_profile')

        return render(request, self.template_name, {'form': form, 'id': pk})
