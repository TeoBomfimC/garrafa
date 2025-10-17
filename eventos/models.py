from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid

TIPOS_EVENTO = [
    ('seminario', 'Seminário'),
    ('palestra', 'Palestra'),
    ('minicurso', 'Minicurso'),
    ('semana', 'Semana Acadêmica'),
]

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=30, choices=TIPOS_EVENTO)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=100)
    vagas = models.PositiveIntegerField()
    organizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='eventos_organizados')

    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='eventos_participados',
        blank=True,
        verbose_name='Participantes Inscritos'
    )
    
    def vagas_disponiveis(self):
        return self.vagas - self.participantes.count()
    
    def __str__(self):
        return self.titulo

class Certificado(models.Model):
    participante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificados_recebidos')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    codigo_autenticidade = models.CharField(max_length=30, unique=True, default=uuid.uuid4)
    data_emissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificado de {self.participante.username} para {self.evento.titulo}"

    class Meta:
        unique_together = ('participante', 'evento')