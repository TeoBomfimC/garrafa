from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

from eventos.models import Evento
from usuarios.models import Usuario
from eventos.utils import registrar_acao

from .serializers import EventoSerializer, InscricaoSerializer
from .throttles import EventListThrottle, InscricaoThrottle


class CustomObtainAuthToken(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key})


class EventoListAPI(generics.ListAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [EventListThrottle]

    def list(self, request, *args, **kwargs):
        registrar_acao(request.user, "Consultou lista de eventos pela API")
        return super().list(request, *args, **kwargs)


class InscreverEventoAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [InscricaoThrottle]

    def post(self, request, evento_id):
        serializer = InscricaoSerializer(data=request.data)

        if not serializer.is_valid():
            registrar_acao(request.user, "Tentou se inscrever via API com dados inválidos")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        usuario_id = serializer.validated_data['usuario_id']

        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            registrar_acao(request.user, "Tentou se inscrever via API: usuário não encontrado")
            return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist:
            registrar_acao(request.user, "Tentou se inscrever via API: evento não encontrado")
            return Response({'detail': 'Evento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if usuario == evento.organizador:
            registrar_acao(request.user, "Tentou se inscrever via API: organizador não pode participar")
            return Response({'detail': 'Organizador não pode se inscrever.'}, status=status.HTTP_400_BAD_REQUEST)

        if evento.vagas_disponiveis() <= 0:
            registrar_acao(request.user, "Tentou se inscrever via API: sem vagas")
            return Response({'detail': 'Não há vagas disponíveis.'}, status=status.HTTP_400_BAD_REQUEST)

        if evento.participantes.filter(id=usuario.id).exists():
            registrar_acao(request.user, "Tentou se inscrever via API: já inscrito")
            return Response({'detail': 'Usuário já inscrito.'}, status=status.HTTP_400_BAD_REQUEST)

        evento.participantes.add(usuario)

        registrar_acao(request.user, f"Inscreveu-se via API no evento {evento.titulo}")

        return Response({'detail': 'Inscrição realizada com sucesso.'}, status=status.HTTP_201_CREATED)


class EventoDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, evento_id):
        try:
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist:
            registrar_acao(request.user, "Tentou consultar evento inexistente via API")
            return Response({'detail': 'Evento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        registrar_acao(request.user, f"Consultou detalhes do evento {evento.titulo} pela API")

        serializer = EventoSerializer(evento)
        return Response(serializer.data, status=status.HTTP_200_OK)


