from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento, Certificado
from .forms import EventoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
import uuid 

UserModel = get_user_model()

def is_organizador(user):
    return user.is_staff or user.is_superuser

@login_required
def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})

@login_required
def detalhe_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'eventos/detalhe_evento.html', {'evento': evento})

@login_required
def criar_evento(request):
    if not is_organizador(request.user):
        messages.error(request, "Acesso negado: Somente organizadores podem criar eventos.")
        return redirect('lista_eventos')
        
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            evento.save()
            messages.success(request, f"Evento '{evento.titulo}' criado com sucesso!")
            return redirect('lista_eventos')
        else:
            messages.error(request, "Erro ao criar evento. Verifique os dados do formulário.")
    else:
        form = EventoForm()
        
    return render(request, 'eventos/form_evento.html', {'form': form})

@login_required
def inscrever_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    usuario = request.user

    if evento.vagas_disponiveis() <= 0:
        messages.error(request, "Desculpe, as vagas para este evento se esgotaram.")
        return redirect('detalhe_evento', evento_id=evento.id)
    
    if evento.participantes.filter(pk=usuario.pk).exists():
        messages.warning(request, "Você já está inscrito neste evento.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if request.method == 'POST':
        evento.participantes.add(usuario)
        messages.success(request, f"Inscrição no evento '{evento.titulo}' realizada com sucesso!")
        return redirect('detalhe_evento', evento_id=evento.id) 
    
    messages.error(request, "Método de requisição inválido para inscrição.")
    return redirect('detalhe_evento', evento_id=evento.id)

@login_required
def emitir_certificado(request, evento_id, usuario_id):
    evento = get_object_or_404(Evento, id=evento_id)
    usuario = get_object_or_404(UserModel, id=usuario_id)

    if request.user != evento.organizador:
        messages.error(request, "Você não tem permissão para emitir certificados para este evento.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if request.method != 'POST':
        messages.error(request, "Método inválido.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if not evento.participantes.filter(id=usuario.id).exists():
        messages.error(request, f"O usuário {usuario.username} não está inscrito neste evento.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if Certificado.objects.filter(participante=usuario, evento=evento).exists():
        messages.warning(request, f"Certificado para {usuario.username} já foi emitido.")
    else:
        codigo = str(uuid.uuid4()).replace('-', '')[:20]
        Certificado.objects.create(
            participante=usuario,
            evento=evento,
            codigo_autenticidade=codigo
        )
        messages.success(request, f"Certificado emitido com sucesso para {usuario.username}!")
    
    return redirect('detalhe_evento', evento_id=evento.id)

@login_required
def visualizar_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)
    
    if request.user != certificado.participante and request.user != certificado.evento.organizador:
        messages.error(request, "Você não tem permissão para visualizar este certificado.")
        return redirect('lista_eventos')

    return render(request, 'eventos/certificado_detalhe.html', {'certificado': certificado})