from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image
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
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos_organizados'
    )
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)

    participantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='eventos_participados',
        blank=True
    )

    def vagas_disponiveis(self):
        return self.vagas - self.participantes.count()

    def clean(self):
        hoje = timezone.now().date()

        if self.data_inicio and self.data_inicio < hoje:
            raise ValidationError('A data de início não pode ser anterior à data atual.')

        if self.data_inicio and self.data_fim and self.data_fim < self.data_inicio:
            raise ValidationError('A data de término deve ser maior ou igual à data de início.')

        if self.banner:
            try:
                img = Image.open(self.banner)
                img.verify()
            except Exception:
                raise ValidationError("O arquivo enviado para o banner não é uma imagem válida.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Certificado(models.Model):
    participante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificados_recebidos'
    )
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    codigo_autenticidade = models.CharField(max_length=30, unique=True, default=uuid.uuid4)
    data_emissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Certificado de {self.participante.username} para {self.evento.titulo}'

    class Meta:
        unique_together = ('participante', 'evento')


class Auditoria(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.acao} - {self.data}"
