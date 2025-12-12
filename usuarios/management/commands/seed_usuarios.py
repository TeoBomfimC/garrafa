from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = "Cria usuários iniciais para teste do sistema"

    def handle(self, *args, **kwargs):

        usuarios = [
            {
                "username": "organizador@sgea.com",
                "email": "organizador@sgea.com",
                "first_name": "Organizador",
                "last_name": "SGEA",
                "perfil": "organizador",
                "senha": "Admin@123"
            },
            {
                "username": "aluno@sgea.com",
                "email": "aluno@sgea.com",
                "first_name": "Aluno",
                "last_name": "SGEA",
                "perfil": "participante",  
                "senha": "Aluno@123"
            },
            {
                "username": "professor@sgea.com",
                "email": "professor@sgea.com",
                "first_name": "Professor",
                "last_name": "SGEA",
                "perfil": "participante",  
                "senha": "Professor@123"
            }
        ]

        for u in usuarios:
            if not Usuario.objects.filter(username=u["username"]).exists():
                novo = Usuario(
                    username=u["username"],
                    email=u["email"],
                    first_name=u["first_name"],
                    last_name=u["last_name"],
                    perfil=u["perfil"]
                )
                novo.set_password(u["senha"])
                novo.save()
                self.stdout.write(self.style.SUCCESS(f"Usuário criado: {u['username']}  Perfil: {u['perfil']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Usuário já existe: {u['username']}"))

        self.stdout.write(self.style.SUCCESS("Processo de seeding concluído!"))
