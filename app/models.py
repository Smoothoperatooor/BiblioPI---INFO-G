from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPOS = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('admin', 'Admin')
    )
    tipo = models.CharField(max_length=10, choices=TIPOS)
    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = ['email', 'tipo']  

    def __str__(self):
        return self.username
    
class Arquivo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Arquivo")
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

