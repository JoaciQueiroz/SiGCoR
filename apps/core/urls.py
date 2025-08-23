from django.urls import path
from .views import HomeView #importa a view que vai ser exibida


app_name='core' #define nemespace

urlpatterns = [
    path('', HomeView.as_view(), name='home')
    
]