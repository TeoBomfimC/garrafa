from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UsuarioRegistroForm 

class RegistroView(CreateView):
    template_name = 'usuarios/registrar.html' 
    form_class = UsuarioRegistroForm
    success_url = reverse_lazy('login')

class LoginCustomizado(LoginView):
    template_name = 'usuarios/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('lista_eventos')