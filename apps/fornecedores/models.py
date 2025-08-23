# apps/fornecedores/models.py
from django.db import models

class Fornecedor(models.Model):
    razao_social = models.CharField(max_length=255, verbose_name="Razão Social")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['razao_social']

    def __str__(self):
        return self.razao_social
