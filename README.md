SGEA — Sistema de Gerenciamento de Eventos Acadêmicos

Plataforma desenvolvida em Django para cadastro, administração e participação em eventos como palestras, minicursos, semanas acadêmicas e seminários.

SGEA — Sistema de Gerenciamento de Eventos Acadêmicos
Plataforma em Django para criação, administração e participação em eventos acadêmicos.

1. Instalação do Projeto

Requisitos
Python 3.10+
Pip

Virtualenv (opcional)
Passos
1.1 Clonar o repositório
git clone https://github.com/SEU_USUARIO/seu_repositorio.git
cd seu_repositorio

1.2 Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

1.3 Instalar dependências
pip install -r requirements.txt

1.4 Aplicar migrações
python manage.py migrate

1.5 Criar usuários iniciais
python manage.py shell

from usuarios.models import Usuario
Usuario.objects.create_user(username="organizador@sgea.com", email="organizador@sgea.com", password="Admin@123", tipo="organizador")
Usuario.objects.create_user(username="aluno@sgea.com", email="aluno@sgea.com", password="Aluno@123", tipo="aluno")
Usuario.objects.create_user(username="professor@sgea.com", email="professor@sgea.com", password="Professor@123", tipo="professor")

exit()

1.6 Executar o servidor
python manage.py runserver

2. Funcionalidades do Sistema

• Cadastro de usuários
Senha forte, confirmação de senha e envio de e-mail automático.

• Login e permissões Perfis: Aluno, Professor, Organizador.

• Eventos Banner com validação Data e hora com validação Professor responsável obrigatório Controle de vagas Impede datas inválidas

• Inscrições Impede duplicadas Impede quando vagas acabam Organizador não pode se inscrever

• Certificados automáticos
Gerados após o término do evento.

• Auditoria
Registra: usuários criados eventos criados/editados/deletados inscrições consultas via API certificados emitidos

3. API REST (Token)

POST /api/token/
{
  "username": "aluno@sgea.com",
  "password": "Aluno@123"
}

GET /api/eventos/
Authorization: Token SEU_TOKEN

POST /api/eventos/<id>/inscrever/
Authorization: Token SEU_TOKEN

4. Regras de Negócio

Evento não pode começar antes de hoje
Data fim ≥ data início
Deve haver professor responsável
Não inscrever mais pessoas que vagas
Não permitir inscrição duplicada
Senha obrigatória forte (mín 8 chars + número + letra + caractere especial)

5. Notificação por E-mail

Ao registrar um usuário, o sistema envia um e-mail contendo:
saudação
logo SGEA
nome do usuário
link de confirmação
Usuários só acessam funcionalidades após confirmação.

6. Identidade Visual

Layout padronizado
CSS customizado
Logotipo + paleta de cores única
HTML seguindo padrões de acessibilidade

7. Guia de Testes
Teste os cenários:

✔ evento com data inválida → erro
✔ inscrição duplicada → erro
✔ sem vagas → erro
✔ organizador tentando se inscrever → proibido
✔ API sem token → 403
✔ certificado só após data fim → OK

8. Estrutura do Projeto

garrafa/
│ manage.py
│ README.md
├── eventos/
├── usuarios/
├── api_rest/
├── sistema_eventos/
└── templates/
