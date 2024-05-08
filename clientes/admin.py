from django.contrib import admin
from .models import Cliente, Recurso, Exigencia, Requerimento, Estado, Servico, Natureza

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'nome', 'data_nascimento', 'telefone_whatsapp', 'telefone', 'arquivo_do_cliente')
    search_fields = ('cpf', 'nome')

admin.site.register(Cliente, ClienteAdmin) # Registra o modelo Cliente no admin do Django da Classe Cliente e da configuração ClienteAdmin

class RequerimentoAdmin(admin.ModelAdmin):
    list_display = ( 'requerente_titular','NB','servico',  'requerente_dependentes', 'tutor_curador', 'instituidor', 'data', 'estado',  'observacao', 'arquivo_do_requerimento')
    search_fields = ('NB', 'requerente_titular__nome', 'requererente_titular__cpf')

admin.site.register(Requerimento, RequerimentoAdmin) # Registra o modelo Requerimento no admin do Django da Classe Requerimento e da configuração RequerimentoAdmin

class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

admin.site.register(Estado, EstadoAdmin) # Registra o modelo Estado no admin do Django da Classe Estado e da configuração EstadoAdmin

class ServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

admin.site.register(Servico, ServicoAdmin) # Registra o modelo Servico no admin do Django da Classe Servico e da configuração ServicoAdmin

class ExigenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'NB', 'data_final_prazo', 'natureza', 'estado', 'arquivo_da_exigencia')
    search_fields = ('NB',) # 'NB__requerente_titular__nome', 'NB__requerente_titular__cpf

admin.site.register(Exigencia, ExigenciaAdmin) # Registra o modelo Exigencia no admin do Django da Classe Exigencia e da configuração ExigenciaAdmin

class RecursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'NB', 'data_final_prazo', 'estado', 'observacao', 'arquivo_do_recurso')
    search_fields = ('NB',)

admin.site.register(Recurso, RecursoAdmin) # Registra o modelo Recurso no admin do Django da Classe Recurso e da configuração RecursoAdmin

class NaturezaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

admin.site.register(Natureza, NaturezaAdmin) # Registra o modelo Natureza no admin do Django da Classe Natureza e da configuração NaturezaAdmin