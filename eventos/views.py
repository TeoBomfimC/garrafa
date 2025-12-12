from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Evento, Certificado
from .forms import EventoForm
from usuarios.models import Usuario
from .utils import registrar_acao
import uuid

def is_org(user):
    return user.perfil in ('organizador', 'admin')

@login_required
def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})

@login_required
def detalhe_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuario_inscrito = evento.participantes.filter(id=request.user.id).exists()
    return render(request, 'eventos/detalhe_evento.html', {
        'evento': evento,
        'usuario_inscrito': usuario_inscrito
    })

@login_required
def criar_evento(request):
    if not is_org(request.user):
        messages.error(request, "Você não tem permissão para criar eventos.")
        return redirect('lista_eventos')

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            evento.save()
            registrar_acao(request.user, f"Criou o evento {evento.titulo}")
            messages.success(request, f"O evento '{evento.titulo}' foi criado.")
            return redirect('lista_eventos')
        messages.error(request, "Erro ao criar evento.")
    else:
        form = EventoForm()

    return render(request, 'eventos/form_evento.html', {'form': form})

@login_required
def inscrever_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuario = request.user

    if is_org(usuario):
        messages.error(request, "Organizadores não podem se inscrever em eventos.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if evento.vagas_disponiveis() <= 0:
        messages.error(request, "Não há vagas disponíveis.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if evento.participantes.filter(id=usuario.id).exists():
        messages.warning(request, "Você já está inscrito.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if request.method == 'POST':
        evento.participantes.add(usuario)
        registrar_acao(usuario, f"Inscreveu-se no evento {evento.titulo}")
        messages.success(request, "Inscrição realizada.")
        return redirect('detalhe_evento', evento_id=evento.id)

    messages.error(request, "Método inválido.")
    return redirect('detalhe_evento', evento_id=evento.id)

@login_required
def cancelar_inscricao(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuario = request.user

    if not evento.participantes.filter(id=usuario.id).exists():
        messages.error(request, "Você não está inscrito.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if request.method == 'POST':
        evento.participantes.remove(usuario)
        registrar_acao(usuario, f"Cancelou inscrição no evento {evento.titulo}")
        messages.success(request, "Inscrição cancelada.")
        return redirect('detalhe_evento', evento_id=evento.id)

    messages.error(request, "Método inválido.")
    return redirect('detalhe_evento', evento_id=evento.id)

@login_required
def emitir_certificado(request, evento_id, usuario_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if not is_org(request.user):
        messages.error(request, "Você não tem permissão para emitir certificados.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if request.method != 'POST':
        messages.error(request, "Método inválido.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if not evento.participantes.filter(id=usuario.id).exists():
        messages.error(request, "O usuário não está inscrito.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if Certificado.objects.filter(participante=usuario, evento=evento).exists():
        messages.warning(request, "Certificado já emitido.")
        return redirect('detalhe_evento', evento_id=evento.id)

    codigo = str(uuid.uuid4()).replace('-', '')[:20]

    Certificado.objects.create(
        participante=usuario,
        evento=evento,
        codigo_autenticidade=codigo
    )

    registrar_acao(request.user, f"Emitiu certificado para {usuario.username} no evento {evento.titulo}")

    messages.success(request, "Certificado emitido.")
    return redirect('detalhe_evento', evento_id=evento.id)

@login_required
def visualizar_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)

    if request.user != certificado.participante and not is_org(request.user):
        messages.error(request, "Você não tem permissão para visualizar este certificado.")
        return redirect('lista_eventos')

    return render(request, 'eventos/certificado_detalhe.html', {'certificado': certificado})

@login_required
def auditoria_lista(request):
    if request.user.perfil != 'admin':
        messages.error(request, "Apenas administradores podem acessar a auditoria.")
        return redirect('lista_eventos')

    from .models import Auditoria
    registros = Auditoria.objects.all().order_by('-data')
    return render(request, 'eventos/auditoria_lista.html', {'registros': registros})
@login_required
def auditoria_filtro(request):
    if request.user.perfil != "organizador":
        messages.error(request, "Apenas organizadores podem acessar a auditoria.")
        return redirect('lista_eventos')

    from .models import Auditoria

    logs = Auditoria.objects.all().order_by('-data')

    usuario_id = request.GET.get("usuario")
    data = request.GET.get("data")

    if usuario_id and usuario_id != "":
        logs = logs.filter(usuario_id=usuario_id)

    if data and data != "":
        logs = logs.filter(data__date=data)

    usuarios = Usuario.objects.all().order_by("username")

    return render(request, "eventos/auditoria_filtro.html", {
        "logs": logs,
        "usuarios": usuarios,
        "f_usuario": usuario_id,
        "f_data": data,
    })
@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if not is_org(request.user):
        messages.error(request, "Você não tem permissão para editar eventos.")
        return redirect('lista_eventos')

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            registrar_acao(request.user, f"Editou o evento {evento.titulo}")
            messages.success(request, "Evento atualizado com sucesso.")
            return redirect('detalhe_evento', evento_id=evento.id)
    else:
        form = EventoForm(instance=evento)

    return render(request, 'eventos/form_evento.html', {'form': form, 'editar': True})
@login_required
def excluir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if not is_org(request.user):
        messages.error(request, "Você não tem permissão para excluir eventos.")
        return redirect('lista_eventos')

    if request.method == 'POST':
        título = evento.titulo
        evento.delete()
        registrar_acao(request.user, f"Excluiu o evento {título}")
        messages.success(request, "Evento excluído com sucesso.")
        return redirect('lista_eventos')

    return render(request, 'eventos/confirmar_exclusao.html', {'evento': evento})
