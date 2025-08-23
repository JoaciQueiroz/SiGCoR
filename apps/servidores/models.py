# apps/servidores/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Setor(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Setor")

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Servidor(AbstractUser):
    matricula = models.CharField(max_length=20, unique=True, verbose_name="Matrícula")
    setor = models.ForeignKey(
        Setor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Setor de Lotação"
    )

    class Meta:
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"

    def __str__(self):
        return self.get_full_name() or self.username