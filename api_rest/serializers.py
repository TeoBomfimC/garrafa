from rest_framework import serializers
from eventos.models import Evento
from usuarios.models import Usuario

class EventoSerializer(serializers.ModelSerializer):
    organizador_username = serializers.CharField(source='organizador.username', read_only=True)
    vagas_disponiveis = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = [
            'id',
            'titulo',
            'tipo',
            'data_inicio',
            'data_fim',
            'horario',
            'local',
            'vagas',
            'vagas_disponiveis',
            'organizador',
            'organizador_username',
            'banner',
        ]
        read_only_fields = [
            'organizador',
            'vagas_disponiveis',
            'organizador_username'
        ]

    def get_vagas_disponiveis(self, obj):
        return obj.vagas_disponiveis()


class InscricaoSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()

    def validate_usuario_id(self, value):
        if not Usuario.objects.filter(id=value).exists():
            raise serializers.ValidationError("Usuário não encontrado.")
        return value
