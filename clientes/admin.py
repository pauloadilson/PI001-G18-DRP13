from django.contrib import admin
from .models import Cliente
from .models import Requerimento
from .models import Estado
from .models import Servico

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'nome', 'data_nascimento', 'telefone_whatsapp', 'telefone')
    search_fields = ('cpf', 'nome')

admin.site.register(Cliente, ClienteAdmin) # Registra o modelo Cliente no admin do Django da Classe Cliente e da configuração ClienteAdmin

class RequerimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'requerente_titular','NB','servico',  'requerente_dependentes', 'tutor_curador', 'instituidor', 'data', 'estado',  'observacao')
    search_fields = ('id', 'NB', 'requerente_titular__nome', 'requererente_titular__cpf')

admin.site.register(Requerimento, RequerimentoAdmin) # Registra o modelo Requerimento no admin do Django da Classe Requerimento e da configuração RequerimentoAdmin

class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

admin.site.register(Estado, EstadoAdmin) # Registra o modelo Estado no admin do Django da Classe Estado e da configuração EstadoAdmin

class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

admin.site.register(Servico, ServicoAdmin) # Registra o modelo Servico no admin do Django da Classe Servico e da configuração ServicoAdmin