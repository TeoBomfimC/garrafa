from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def enviar_email_confirmacao(usuario):
    link = f"http://localhost:8000/usuarios/confirmar/{usuario.codigo_confirmacao}/"
    html = render_to_string('usuarios/email_confirmacao.html', {'usuario': usuario, 'link': link})
    texto = strip_tags(html)
    send_mail(
        'Confirmação de Cadastro - SGEA',
        texto,
        settings.EMAIL_HOST_USER,
        [usuario.email],
        html_message=html
    )
