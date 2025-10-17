from django.contrib.auth.models import AbstractUser
from django.db import models

PERFIS = [
    ('organizador', 'Organizador'),
    ('aluno', 'Aluno'),
    ('professor', 'Professor'),
]

class Usuario(AbstractUser):
    # CAMPOS CUSTOMIZADOS
    telefone = models.CharField(max_length=15, blank=True, null=True)
    instituicao = models.CharField(max_length=100, blank=True, null=True)
    perfil = models.CharField(max_length=20, choices=PERFIS, default='aluno')
    
    # CAMPOS DE PERMISSÃO COM related_name CORRIGIDO (OBRIGATÓRIO)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set', 
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    def __str__(self):
        return self.username