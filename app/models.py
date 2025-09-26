from django.db import models
    
class Arquivo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Arquivo")
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"

