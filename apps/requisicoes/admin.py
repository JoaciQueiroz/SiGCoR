from django.contrib import admin
from .models import Requisicao, ItemRequisicaoMaterial, ItemRequisicaoServico

class ItemMaterialInline(admin.TabularInline):
    model = ItemRequisicaoMaterial
    extra = 1

class ItemServicoInline(admin.TabularInline):
    model = ItemRequisicaoServico
    extra = 1

@admin.register(Requisicao)
class RequisicaoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'solicitante', 'data_solicitacao', 'status')
    list_filter = ('status', 'tipo', 'setor_solicitante')
    search_fields = ('solicitante__first_name', 'justificativa')

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.tipo == 'MATERIAL':
                return [ItemMaterialInline]
            elif obj.tipo == 'SERVICO':
                return [ItemServicoInline]
        return []