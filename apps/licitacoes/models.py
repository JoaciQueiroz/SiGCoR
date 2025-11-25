# apps/licitacoes/models.py

from django.db import models

class Modalidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Modalidade de Licitação"
        verbose_name_plural = "Modalidades de Licitação"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Licitacao(models.Model):
    numero_processo = models.CharField(max_length=50, unique=True, verbose_name="Número do Processo")
    modalidade = models.ForeignKey(
        Modalidade,
        on_delete=models.PROTECT, # Impede que uma modalidade em uso seja excluída
        verbose_name="Modalidade"
    )
    objeto = models.TextField()
    data_abertura = models.DateField(verbose_name="Data de Abertura")
    
    # === NOVOS CAMPOS ===
    data_fim = models.DateField(
        verbose_name="Data de Encerramento", 
        null=True, 
        blank=True, 
        help_text="Data prevista para o fim da licitação ou validade da ata."
    )
    
    valor_global = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name="Valor Global Estimado",
        default=0.00
    )

    class Meta:
        verbose_name = "Licitação"
        verbose_name_plural = "Licitações"
        ordering = ['-data_abertura']

    def __str__(self):
        return f"{self.numero_processo} - {self.modalidade.nome}"
