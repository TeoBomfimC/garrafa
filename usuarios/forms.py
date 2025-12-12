from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from usuarios.models import Usuario
import re

class UsuarioRegistroForm(UserCreationForm):
    """
    Formulário de registro com validações:
    email único e válido, telefone no padrão (XX) XXXXX-XXXX,
    e regras de senha fortes.
    """

    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'telefone',
            'instituicao',
            'perfil',
            'password1',
            'password2'
        ]
        labels = {
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'telefone': 'Telefone',
            'instituicao': 'Instituição de ensino',
            'perfil': 'Perfil',
            'password1': 'Senha',
            'password2': 'Confirme a senha'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('O email é obrigatório.')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Informe um email válido.')
        if Usuario.objects.filter(email__iexact=email).exists():
            raise ValidationError('Este email já está em uso.')
        return email

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            padrao = r'^\(\d{2}\)\s?\d{4,5}-\d{4}$'
            if not re.match(padrao, telefone):
                raise ValidationError('Telefone deve estar no formato (XX) XXXXX-XXXX')
        return telefone

    def clean_password1(self):
        senha = self.cleaned_data.get('password1')
        if senha:
            if len(senha) < 8:
                raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
            if not re.search(r'[A-Z]', senha):
                raise ValidationError('A senha deve conter ao menos uma letra maiúscula.')
            if not re.search(r'[a-z]', senha):
                raise ValidationError('A senha deve conter ao menos uma letra minúscula.')
            if not re.search(r'\d', senha):
                raise ValidationError('A senha deve conter ao menos um número.')
            if not re.search(r'[\W_]', senha):
                raise ValidationError('A senha deve conter ao menos um caractere especial.')
        return senha

    def clean(self):
        dados = super().clean()
        perfil = dados.get('perfil')
        instituicao = dados.get('instituicao')
        if perfil in ['aluno', 'professor'] and not instituicao:
            self.add_error('instituicao', 'Alunos e professores devem informar a instituição.')
        return dados

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data.get('email')
        if commit:
            usuario.save()
        return usuario
