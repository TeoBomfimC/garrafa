from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UsuarioRegistroForm
from .email_utils import enviar_email_confirmacao
from .models import Usuario

from eventos.utils import registrar_acao   # <<< IMPORTANTE


class RegistroView(CreateView):
    template_name = 'usuarios/registrar.html'
    form_class = UsuarioRegistroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.is_active = False
        usuario.save()

        registrar_acao(usuario, "Realizou cadastro no sistema")

        enviar_email_confirmacao(usuario)

        registrar_acao(usuario, "E-mail de confirmação enviado")

        messages.success(self.request, "Cadastro realizado! Verifique seu e-mail para confirmar a conta.")
        return redirect('login')


class LoginCustomizado(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        ...
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user

        if user.perfil == 'organizador':
            return reverse_lazy('dashboard_organizador')

        if user.perfil == 'professor':
            return reverse_lazy('dashboard_professor')

        return reverse_lazy('dashboard_participante')



@login_required
def logout_usuario(request):
    registrar_acao(request.user, "Realizou logout do sistema")
    logout(request)
    return redirect('login')


@login_required
def dashboard_admin(request):
    return render(request, 'usuarios/dashboard_admin.html')


@login_required
def dashboard_organizador(request):
    return render(request, 'usuarios/dashboard_organizador.html')


@login_required
def dashboard_participante(request):
    return render(request, 'usuarios/dashboard_participante.html')


def confirmar_cadastro(request, codigo):
    usuario = get_object_or_404(Usuario, codigo_confirmacao=codigo)
    usuario.is_confirmado = True
    usuario.is_active = True
    usuario.save()

    registrar_acao(usuario, "Confirmou o cadastro via e-mail")

    messages.success(request, "Cadastro confirmado! Agora você pode fazer login.")
    return redirect('login')
