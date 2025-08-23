from django.contrib import admin
from .models import Produto, MovimentacaoEstoque

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'unidade_medida', 'saldo_estoque')
    search_fields = ('descricao',)

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('data', 'produto', 'tipo', 'quantidade')
    list_filter = ('tipo', 'produto')
    search_fields = ('produto__descricao',)
