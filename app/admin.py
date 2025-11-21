from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.register(Arquivo)
admin.site.register(Topico)
admin.site.register(Mensagem)