# apps/contratos/models.py

from django.db import models
from django.db.models import Sum
from sigcor.settings import AUTH_USER_MODEL # Importa o modelo de usuário customizado
from apps.fornecedores.models import Fornecedor
from apps.licitacoes.models import Licitacao
from apps.estoque.models import Produto
from django.urls import reverse

class Contrato(models.Model):
    STATUS_CHOICES = (
        ('VIGENTE', 'Vigente'),
        ('ENCERRADO', 'Encerrado'),
        ('SUSPENSO', 'Suspenso'),
        ('RESCINDIDO', 'Rescindido'),
    )
    licitacao_origem = models.ForeignKey(Licitacao,
        on_delete=models.PROTECT,
        verbose_name="Licitação de Origem",
        related_name="contratos"
    )
    fornecedor = models.ForeignKey(Fornecedor, 
        on_delete=models.PROTECT, 
        related_name="contratos_fornecedores")
    fiscal = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contratos_fiscalizados"
    )
    numero_contrato = models.CharField(max_length=50, verbose_name="Número do Contrato")
    ano_contrato = models.PositiveIntegerField(verbose_name="Ano do Contrato")
    objeto = models.TextField()
    valor_global = models.DecimalField(max_digits=12, decimal_places=2)
    data_assinatura = models.DateField(verbose_name="Data de Assinatura")
    data_vigencia_fim = models.DateField(verbose_name="Fim da Vigência")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='VIGENTE')
    
    @property
    def valor_total_pago(self):
        soma = self.pagamentos.aggregate(total=Sum('valor'))['total']
        return soma if soma is not None else 0
    
    @property
    def saldo_a_pagar(self):
        return self.valor_global - self.valor_total_pago

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        unique_together = ('numero_contrato', 'ano_contrato')
        ordering = ['-ano_contrato', '-numero_contrato']

    def __str__(self):
        return f"Contrato {self.numero_contrato}/{self.ano_contrato}"
    
    def get_absolute_url(self):
        return reverse('contratos:detalhe_contrato', kwargs={'pk': self.pk})
    
class ItemContrato(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="itens")
    produto_catalogo = models.ForeignKey(
        Produto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Produto do Catálogo"
    )
    descricao = models.CharField(max_length=255, verbose_name="Descrição do Item")
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Item do Contrato"
        verbose_name_plural = "Itens do Contrato"

    def __str__(self):
        return self.descricao

class Pagamento(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="pagamentos")
    data_pagamento = models.DateField(verbose_name="Data do Pagamento")
    valor = models.DecimalField(max_digits=12, decimal_places=2) 
    observacao = models.TextField(verbose_name="Observação", blank=True, null=True)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-data_pagamento']

    def __str__(self):
        # Ajustado para usar o novo nome do campo 'valor'
        return f"Pagamento de R$ {self.valor} em {self.data_pagamento.strftime('%d/%m/%Y')}"

class Recebimento(models.Model):
    item_contrato = models.ForeignKey(ItemContrato, on_delete=models.PROTECT, related_name="recebimentos")
    quantidade_recebida = models.DecimalField(max_digits=10, decimal_places=2)
    data_recebimento = models.DateField(verbose_name="Data do Recebimento")

    class Meta:
        verbose_name = "Recebimento de Item"
        verbose_name_plural = "Recebimentos de Itens"
        ordering = ['-data_recebimento']

    def __str__(self):
        return f"{self.quantidade_recebida}x {self.item_contrato.descricao}"

class Documento(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="documentos")
    descricao = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='contratos_documentos/')

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.descricao

