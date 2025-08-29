# ARQUIVO: apps/core/views.py

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Importe os modelos dos outros apps que você precisará consultar
from apps.contratos.models import Contrato
from apps.requisicoes.models import Requisicao

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # --- Contagem de Contratos por Status ---
        context['contratos_vigentes'] = Contrato.objects.filter(status='VIGENTE').count()
        context['contratos_encerrados'] = Contrato.objects.filter(status='ENCERRADO').count()
        context['contratos_suspensos'] = Contrato.objects.filter(status='SUSPENSO').count()
     
        # ============== INÍCIO DA CORREÇÃO APLICADA   
        
        # --- Contagem de Requisições por Status ---
        # CORREÇÃO: Use os valores em MAIÚSCULAS que são armazenados no banco de dados.
        context['requisicoes_abertas'] = Requisicao.objects.filter(status='ABERTA').count()
        context['requisicoes_aprovadas'] = Requisicao.objects.filter(status='APROVADA').count()
        context['requisicoes_reprovadas'] = Requisicao.objects.filter(status='REPROVADA').count()
        context['requisicoes_atendidas'] = Requisicao.objects.filter(status='ATENDIDA').count()
        
        # =============== FIM DA CORREÇÃO APLICADA 
        
        return context