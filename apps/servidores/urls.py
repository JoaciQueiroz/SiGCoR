from django.urls import path

from .views import (
    SetorListView,
    SetorCreateView,
    SetorUpdateView,
    SetorDeleteView
)

app_name = 'servidores'

urlpatterns = [
    path('', SetorListView.as_view(), name= 'lista_setores'),
    path('novo/', SetorCreateView.as_view(), name= 'cria_setor'),
    path('<int:pk>/editar/', SetorUpdateView.as_view(), name='edita_setor'),
    path('<int:pk>/excluir/', SetorDeleteView.as_view(), name='exclui_setor'),
]