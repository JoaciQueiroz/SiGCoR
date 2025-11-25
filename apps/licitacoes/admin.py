from django.contrib import admin
from .models import Modalidade, Licitacao

admin.site.register(Modalidade)

@admin.register(Licitacao)
class LicitacaoAdmin(admin.ModelAdmin):
    list_display = ('numero_processo', 'modalidade', 'objeto', 'data_abertura', 'data_fim', 'valor_global')
    search_fields = ('numero_processo', 'objeto')
    list_filter = ('modalidade', 'data_abertura')
   