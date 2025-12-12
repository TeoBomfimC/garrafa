from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

PERFIS = [
    ('organizador', 'Organizador'),
    ('aluno', 'Aluno'),
    ('professor', 'Professor'),
]

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=15, blank=True, null=True)
    instituicao = models.CharField(max_length=100, blank=True, null=True)
    perfil = models.CharField(max_length=20, choices=PERFIS, default='aluno')
    codigo_confirmacao = models.UUIDField(default=uuid.uuid4, unique=True)
    is_confirmado = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username
