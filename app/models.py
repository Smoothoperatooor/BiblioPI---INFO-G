from django.db import models
    
class Arquivo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Arquivo")
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

class Usuario(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do usuario")
    email = models.CharField(max_length=100, verbose_name="Email do usuario")
    senha = models.CharField(max_length=100, verbose_name="Senha do usuario")
    funcao = models.CharField(max_length=100, verbose_name="Função do usuario")

    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"