from django.db import models
from django.contrib.auth.models import AbstractUser

class Arquivo(models.Model):
    CATEGORIAS = (
        ('trabalho', 'Trabalho'),
        ('projeto', 'Projeto'),
        ('pesquisa', 'Pesquisa'),
        ('outro', 'Outro')
    )
    
    nome = models.CharField(max_length=200, verbose_name="Nome do Arquivo")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    arquivo = models.FileField(upload_to='arquivos/', verbose_name="Arquivo", blank=True, null=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='trabalho')
    data_upload = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
