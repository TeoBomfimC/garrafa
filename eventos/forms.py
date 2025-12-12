from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        exclude = ('organizador', 'participantes')
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_data_inicio(self):
        data = self.cleaned_data.get('data_inicio')
        hoje = timezone.now().date()
        if data and data < hoje:
            raise ValidationError('A data de início não pode ser anterior à data atual.')
        return data

    def clean_data_fim(self):
        inicio = self.cleaned_data.get('data_inicio')
        fim = self.cleaned_data.get('data_fim')
        if inicio and fim and fim < inicio:
            raise ValidationError('A data de término deve ser maior ou igual à data de início.')
        return fim

    def clean_vagas(self):
        vagas = self.cleaned_data.get('vagas')
        if vagas is not None and vagas <= 0:
            raise ValidationError('O número de vagas deve ser maior que zero.')
        return vagas

    def clean_banner(self):
        banner = self.cleaned_data.get('banner')
        if banner:
            tipo = getattr(banner, 'content_type', None)
            if tipo and not tipo.startswith('image/'):
                raise ValidationError('O banner enviado deve ser uma imagem válida.')
        return banner

    def clean(self):
        dados = super().clean()
        inicio = dados.get('data_inicio')
        fim = dados.get('data_fim')
        if inicio and fim and fim < inicio:
            self.add_error('data_fim', 'A data de término não pode ser antes da data inicial.')
        return dados
