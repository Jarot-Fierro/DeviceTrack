from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from user.forms import CustomLoginForm


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
        self.request.session.set_expiry(0)  # Cierra sesión al cerrar navegador
        return super().form_valid(form)

    def redirect_to_success_url(self):
        return redirect(self.get_success_url())


@method_decorator(never_cache, name='dispatch')
class LogoutViewCustom(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        request.session.flush()  # Elimina todos los datos de sesión
        return response
