# apps/estoque/models.py
from django.db import models
from apps.fornecedores.models import Fornecedor

class Produto(models.Model):
    descricao = models.CharField(max_length=255, unique=True, verbose_name="Descrição")
    unidade_medida = models.CharField(max_length=20, verbose_name="Unidade de Medida")
    saldo_estoque = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Saldo em Estoque"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['descricao']

    def __str__(self):
        return self.descricao

class MovimentacaoEstoque(models.Model):
    TIPO_MOVIMENTACAO = (
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    )
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="movimentacoes")
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO)
    data = models.DateTimeField(auto_now_add=True, verbose_name="Data da Movimentação")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data']

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.quantidade} - {self.produto.descricao}"