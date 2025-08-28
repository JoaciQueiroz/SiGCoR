from django.urls import path
from .views import HomeView #importa a view que vai ser exibida
from django.contrib.auth import views as auth_views
from .views import HomeView


app_name='core' #define nemespace

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    #rota de login
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),    
]