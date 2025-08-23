from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Servidor, Setor

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Servidor)
class ServidorAdmin(UserAdmin):
    model = Servidor
    fieldsets = UserAdmin.fieldsets + (
        ('Dados Complementares', {'fields': ('matricula', 'setor')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'setor')
    list_filter = ('setor', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('first_name', 'last_name', 'email', 'matricula')
