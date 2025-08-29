from django.urls import path
from django.contrib.auth import views as auth_views
# Ajuste este import para pegar a nova view
from .views import DashboardView

app_name = 'core'

urlpatterns = [
    # Aponte a rota raiz para a DashboardView
    path('', DashboardView.as_view(), name='home'),
    
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html'
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(
        next_page='core:login'
    ), name='logout'),
]