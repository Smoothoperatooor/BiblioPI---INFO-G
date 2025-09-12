from django.contrib import admin
from django.contrib.auth.models import Group

# Garante que os grupos existem sempre que o admin for carregado
def create_default_groups():
    grupos = ["Aluno", "Professor", "Admin"]
    for nome in grupos:
        Group.objects.get_or_create(name=nome)

# Chama a função logo que o admin é carregado
create_default_groups()