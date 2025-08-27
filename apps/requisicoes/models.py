# apps/requisicoes/models.py

from django.db import models
from django.utils import timezone
from django.db import models, transaction
from django.core.exceptions import ValidationError
from sigcor.settings import AUTH_USER_MODEL
from apps.servidores.models import Setor
from apps.estoque.models import Produto

class Requisicao(models.Model):
    """
    Modelo central que representa uma solicitação, que pode ser tanto
    para materiais de estoque quanto para a medição de um serviço.
    """
    TIPO_CHOICES = (
        ('MATERIAL', 'Requisição de Material'),
        ('SERVICO', 'Requisição de Serviço'),
    )
    STATUS_CHOICES = (
        ('ABERTA', 'Aberta'),
        ('APROVADA', 'Aprovada'),
        ('REPROVADA', 'Reprovada'),
        ('ATENDIDA', 'Atendida'),
    )

    tipo = models.CharField(
        max_length=8,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Requisição"
    )
    solicitante = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="requisicoes_solicitadas",
        verbose_name="Solicitante"
    )
    numero_requisicao = models.CharField(max_length=25, unique=True, editable=False, null=True, blank=True)
    setor_solicitante = models.ForeignKey(Setor, on_delete=models.PROTECT, verbose_name="Setor Solicitante")
    data_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Solicitação", editable=False)
    justificativa = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ABERTA')
      
    class Meta:
        verbose_name = "Requisição"
        verbose_name_plural = "Requisições"
        ordering = ['-data_solicitacao']
    
    def __str__(self):   
        identificador = self.numero_requisicao or f"Requisição #{self.pk or 'Nova'}"
        nome_setor = self.setor_solicitante.nome if self.setor_solicitante else "Setor não definido"   
        return f"{identificador} ({self.get_tipo_display()}) - {nome_setor}"
    
    def save(self, *args, **kwargs):
      
        if not self.pk:
            with transaction.atomic():
           
                hoje = timezone.now()
                ano = hoje.year
                mes = hoje.month

                ultima_requisicao = Requisicao.objects.filter(
                    data_solicitacao__year=ano,
                    data_solicitacao__month=mes
                ).order_by('-data_solicitacao').first()

                if ultima_requisicao and ultima_requisicao.numero_requisicao:
                    numero_antigo = int(ultima_requisicao.numero_requisicao[:-6])
                    novo_sequencial = numero_antigo + 1
                else:
                    novo_sequencial = 1
                
                self.numero_requisicao = f"{novo_sequencial}{mes:02d}{ano}"

        super().save(*args, **kwargs)  
        
    @property
    def valor_total(self):
        """Calcula o valor total da requisição com base no seu tipo."""
        total = 0
        if self.tipo == 'MATERIAL':
            # A lógica de valor para material pode ser implementada se o produto tiver um preço de custo.
            # Por enquanto, focamos na quantidade.
            return self.itens_material.count() # Retorna a quantidade de itens diferentes
        elif self.tipo == 'SERVICO':
            # Soma o valor de todos os serviços associados.
            total = self.itens_servico.aggregate(models.Sum('valor'))['valor__sum'] or 0
        return total


class ItemRequisicaoMaterial(models.Model):
    """
    Representa um item de material em uma requisição, no estilo de uma nota fiscal.
    Este modelo só deve ser usado se a Requisição for do tipo 'MATERIAL'.
    """
    requisicao = models.ForeignKey(
        Requisicao,
        on_delete=models.CASCADE,
        related_name="itens_material",
        limit_choices_to={'tipo': 'MATERIAL'} # Garante que só possa ser associado a requisições de material
    )
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name="Produto")
    quantidade_solicitada = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Item de Material"
        verbose_name_plural = "Itens de Material"

    def __str__(self):
        return f"{self.quantidade_solicitada}x {self.produto.descricao}"

class ItemRequisicaoServico(models.Model):
    """
    Representa um serviço ou medição em uma requisição.
    Este modelo só deve ser usado se a Requisição for do tipo 'SERVICO'.
    """
    requisicao = models.ForeignKey(
        Requisicao,
        on_delete=models.CASCADE,
        related_name="itens_servico",
        limit_choices_to={'tipo': 'SERVICO'} # Garante que só possa ser associado a requisições de serviço
    )
    descricao = models.CharField(max_length=255, verbose_name="Descrição do Serviço/Medição")
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor (R$)")

    class Meta:
        verbose_name = "Item de Serviço"
        verbose_name_plural = "Itens de Serviço"

    def __str__(self):
        return f"Serviço: {self.descricao} - R$ {self.valor}"

