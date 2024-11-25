from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

class PefilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefone', 'data_nascimento', 'cpf','cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade']

   
admin.site.register(models.Perfil, PefilAdmin)

