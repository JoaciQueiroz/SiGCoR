from django.contrib import admin
from .models import Contrato, ItemContrato, Pagamento, Recebimento, Documento

class ItemContratoInline(admin.TabularInline):
    model = ItemContrato
    extra = 1

class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 1

class DocumentoInline(admin.TabularInline):
    model = Documento
    extra = 1

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'fornecedor', 'valor_global', 'data_vigencia_fim', 'status')
    list_filter = ('status', 'fornecedor', 'ano_contrato')
    search_fields = ('numero_contrato', 'objeto', 'fornecedor__razao_social')
    inlines = [ItemContratoInline, PagamentoInline, DocumentoInline]

@admin.register(Recebimento)
class RecebimentoAdmin(admin.ModelAdmin):
   # list_display = ('__str__', 'item_pedido', 'data_recebimento')
   # search_fields = ('item_contrato__descricao',)
  list_display = ['id', 'get_produto_descricao', 'data_recebimento', 'quantidade_recebida']
   # Isso ajuda a mostrar o nome real do item na tabela do admin
  def get_produto_descricao(self, obj):
      # Navega: Recebimento -> ItemPedido -> ItemContrato -> Descrição
      return obj.item_pedido.item_contrato.descricao
  get_produto_descricao.short_description = 'Produto'