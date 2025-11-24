# apps/contratos/models.py

from sigcor.settings import AUTH_USER_MODEL
from django.db import models
from django.db.models import Sum
from datetime import date
from django.core.exceptions import ValidationError
from apps.fornecedores.models import Fornecedor
from apps.licitacoes.models import Licitacao
from apps.estoque.models import Produto
from django.urls import reverse

# ==============================================================================
# 1. CONTRATO
# ==============================================================================
class Contrato(models.Model):
    STATUS_CHOICES = (
        ('VIGENTE', 'Vigente'),
        ('ENCERRADO', 'Encerrado'),
        ('SUSPENSO', 'Suspenso'),
        ('RESCINDIDO', 'Rescindido'),
    )
    licitacao_origem = models.ForeignKey(Licitacao, on_delete=models.PROTECT, verbose_name="Licitação de Origem", related_name="contratos")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name="contratos_fornecedores")
    fiscal = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="contratos_fiscalizados")
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

# ==============================================================================
# 2. ITEM DO CONTRATO
# ==============================================================================
class ItemContrato(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="itens")
    produto_catalogo = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Produto do Catálogo")
    descricao = models.CharField(max_length=255, verbose_name="Descrição do Item")
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    
    @property
    def total_solicitado_em_pedidos(self):
        """Soma a quantidade total deste item que foi solicitada em TODOS os pedidos de entrega."""
        soma = self.pedidos_associados.aggregate(total=models.Sum('quantidade_solicitada'))['total']
        return soma if soma is not None else 0

    @property
    def saldo_disponivel_para_solicitar(self):
        """
        Calcula quanto do contrato ainda pode ser transformado em Pedido de Entrega.
        (Qtd Contratada - Qtd já pedida ao fornecedor)
        """
        return self.quantidade - self.total_solicitado_em_pedidos

    class Meta:
        verbose_name = "Item do Contrato"
        verbose_name_plural = "Itens do Contrato"

    def __str__(self):
        return self.descricao

# ==============================================================================
# 3. PEDIDO DE ENTREGA (CABEÇALHO)
# ==============================================================================
class PedidoEntregaFornecedor(models.Model):
    STATUS_PEDIDO = [
        ('PENDENTE', 'Pendente'),
        ('PARCIAL', 'Parcialmente Atendido'),
        ('ATENDIDO', 'Atendido'),
        ('CANCELADO', 'Cancelado'),
    ]

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="pedidos_entrega", verbose_name="Contrato Associado")
    data_solicitacao = models.DateField(default=date.today, verbose_name="Data da Solicitação")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")
    status = models.CharField(max_length=10, choices=STATUS_PEDIDO, default='PENDENTE', verbose_name="Status do Pedido")

    class Meta:
        verbose_name = "Pedido de Entrega ao Fornecedor"
        verbose_name_plural = "Pedidos de Entrega ao Fornecedor"
        ordering = ['-data_solicitacao']

    def __str__(self):
        return f"Pedido Nº {self.pk} - {self.get_status_display()}"

    def atualizar_status(self):
        """Verifica os recebimentos e atualiza o status do pedido automaticamente."""
        total_solicitado = self.itens_solicitados.aggregate(total=models.Sum('quantidade_solicitada'))['total'] or 0
        
        total_recebido = 0
        for item in self.itens_solicitados.all():
            total_recebido += item.total_recebido_deste_item_no_pedido

        if total_recebido == 0:
            self.status = 'PENDENTE'
        elif total_recebido >= total_solicitado:
            self.status = 'ATENDIDO'
        else:
            self.status = 'PARCIAL'
        self.save()

# ==============================================================================
# 4. ITEM DO PEDIDO DE ENTREGA (COM A VALIDAÇÃO SOLICITADA)
# ==============================================================================
class ItemPedidoEntrega(models.Model):
    pedido_entrega = models.ForeignKey(PedidoEntregaFornecedor, on_delete=models.CASCADE, related_name="itens_solicitados")
    item_contrato = models.ForeignKey(ItemContrato, on_delete=models.PROTECT, related_name="pedidos_associados")
    quantidade_solicitada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade Solicitada")

    @property
    def total_recebido_deste_item_no_pedido(self):
        """Soma quanto já chegou fisicamente deste pedido específico."""
        soma = self.recebimentos.aggregate(total=models.Sum('quantidade_recebida'))['total']
        return soma if soma is not None else 0

    @property
    def saldo_a_receber_do_pedido(self):
        """Quanto falta o caminhão entregar deste pedido."""
        return self.quantidade_solicitada - self.total_recebido_deste_item_no_pedido

    # --------------------------------------------------------------------------
    # MÉTODO CLEAN: AQUI ESTÁ A VALIDAÇÃO SOLICITADA
    # --------------------------------------------------------------------------
    def clean(self):
        # Garante que os campos necessários estão preenchidos antes de validar
        if not self.item_contrato_id or not self.quantidade_solicitada:
            return

        # 1. Obtém o saldo atual disponível no contrato
        saldo_disponivel = self.item_contrato.saldo_disponivel_para_solicitar

        # 2. Lógica de Edição:
        # Se estamos editando um item já existente (self.pk existe), 
        # precisamos "devolver" a quantidade antiga ao saldo para recalcular corretamente.
        # Ex: Tinha 100 de saldo. Pedi 50. Saldo virou 50.
        # Agora quero editar de 50 para 80.
        # Conta: Saldo Atual (50) + Antigo (50) = 100. Novo pedido (80) <= 100? Sim. OK.
        if self.pk:
            try:
                item_existente = ItemPedidoEntrega.objects.get(pk=self.pk)
                saldo_disponivel += item_existente.quantidade_solicitada
            except ItemPedidoEntrega.DoesNotExist:
                pass # Caso raro de race condition, segue o baile

        # 3. Validação Principal: Pedido vs Saldo Contrato
        if self.quantidade_solicitada > saldo_disponivel:
            raise ValidationError({
                'quantidade_solicitada': f"A quantidade solicitada ({self.quantidade_solicitada}) excede o saldo disponível no contrato ({saldo_disponivel})."
            })
        
        # 4. Validação de Zero/Negativo
        if self.quantidade_solicitada <= 0:
            raise ValidationError({
                'quantidade_solicitada': "A quantidade solicitada deve ser maior que zero."
            })

    def save(self, *args, **kwargs):
        # Chama o clean() automaticamente antes de salvar
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Item de Pedido de Entrega"
        verbose_name_plural = "Itens de Pedido de Entrega"
        unique_together = ('pedido_entrega', 'item_contrato')
        ordering = ['item_contrato__descricao']

    def __str__(self):
        return f"{self.quantidade_solicitada} de {self.item_contrato.descricao}"

# ==============================================================================
# 5. PAGAMENTO
# ==============================================================================
class Pagamento(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="pagamentos")
    data_pagamento = models.DateField(verbose_name="Data do Pagamento")
    valor = models.DecimalField(max_digits=12, decimal_places=2) 
    observacao = models.TextField(verbose_name="Observação", blank=True, null=True)

    def clean(self):
        if not self.contrato_id or not self.valor:
            return
            
        saldo_contrato = self.contrato.saldo_a_pagar
        
        if self.pk:
            try:
                pagamento_antigo = Pagamento.objects.get(pk=self.pk)
                saldo_contrato += pagamento_antigo.valor
            except Pagamento.DoesNotExist:
                pass

        if self.valor > saldo_contrato:
            raise ValidationError({
                'valor': f"O valor (R$ {self.valor}) excede o saldo financeiro do contrato (R$ {saldo_contrato})."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        ordering = ['-data_pagamento']

    def __str__(self):
        return f"Pagamento R$ {self.valor}"

# ==============================================================================
# 6. RECEBIMENTO
# ==============================================================================
class Recebimento(models.Model):
    item_pedido_entrega = models.ForeignKey(ItemPedidoEntrega, on_delete=models.PROTECT, related_name="recebimentos", verbose_name="Item do Pedido")
    quantidade_recebida = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade Recebida")
    data_recebimento = models.DateField(verbose_name="Data do Recebimento", default=date.today)

    def clean(self):
        if not self.item_pedido_entrega_id or not self.quantidade_recebida:
            return

        saldo_pedido = self.item_pedido_entrega.saldo_a_receber_do_pedido

        if self.pk:
            try:
                recebimento_antigo = Recebimento.objects.get(pk=self.pk)
                saldo_pedido += recebimento_antigo.quantidade_recebida
            except Recebimento.DoesNotExist:
                pass

        if self.quantidade_recebida > saldo_pedido:
            raise ValidationError({
                'quantidade_recebida': f"A quantidade ({self.quantidade_recebida}) excede o que falta entregar deste pedido ({saldo_pedido})."
            })

        if self.quantidade_recebida <= 0:
            raise ValidationError({'quantidade_recebida': "A quantidade deve ser maior que zero."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Recebimento de Item"
        verbose_name_plural = "Recebimentos de Itens"
        ordering = ['-data_recebimento']

    def __str__(self):
        return f"Recebimento: {self.quantidade_recebida}"

# ==============================================================================
# 7. DOCUMENTO
# ==============================================================================
class Documento(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="documentos")
    descricao = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='contratos_documentos/')

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.descricao