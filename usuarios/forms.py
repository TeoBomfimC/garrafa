from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'telefone', 'instituicao', 'perfil', 'password1', 'password2']
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'telefone': 'Telefone',
            'instituicao': 'Instituição de ensino',
            'perfil': 'Perfil',
            'password1': 'Senha',
            'password2': 'Confirme a senha',
        }

    def clean(self):
        cleaned_data = super().clean()
        perfil = cleaned_data.get('perfil')
        instituicao = cleaned_data.get('instituicao')

        if perfil in ['aluno', 'professor'] and not instituicao:
            self.add_error('instituicao', 'Alunos e professores devem informar a instituição de ensino.')

        return cleaned_data
