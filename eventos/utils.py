from .models import Auditoria

def registrar_acao(usuario, acao):
    Auditoria.objects.create(usuario=usuario, acao=acao)
