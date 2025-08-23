from django.urls import path
from .views import(
    ProdutoListView,
    ProdutoCreateView,
    ProdutoUpdateView,
    ProdutoDeleteView
)

app_name = 'estoque'

urlpatterns = [
    path('', ProdutoListView.as_view(), name='lista_produtos'),
    path('novo/', ProdutoCreateView.as_view(), name='cria_produto'),
    path('<int:pk>/editar/', ProdutoUpdateView.as_view(), name='edita_produto'),
    path('<int:pk>/excluir/', ProdutoDeleteView.as_view(), name='exclui_produto'),
]