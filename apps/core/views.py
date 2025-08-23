from django.shortcuts import render
from django .views.generic import TemplateView

class HomeView(TemplateView):
    #informando qual o template
    template_name = 'core/home.html'

# Create your views here.
