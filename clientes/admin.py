from django.contrib import admin
from .models import Cliente, Recurso, Exigencia, Requerimento, Estado, Servico, Natureza

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'nome', 'data_nascimento', 'telefone_whatsapp', 'telefone', 'arquivo_do_cliente')
    search_fields = ('cpf', 'nome')

admin.site.register(Cliente, ClienteAdmin) # Registra o modelo Cliente no admin do Django da Classe Cliente e da configuração ClienteAdmin

class RequerimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'requerente_titular','NB','servico',  'requerente_dependentes', 'tutor_curador', 'instituidor', 'data', 'estado',  'observacao', 'arquivo_do_requerimento')
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

class RecursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'NB', 'protocolo', 'data', 'estado', 'observacao', 'arquivo_do_recurso')
    search_fields = ('NB', 'protocolo')

admin.site.register(Recurso, RecursoAdmin) # Registra o modelo Recurso no admin do Django da Classe Recurso e da configuração RecursoAdmin

class ExigenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'NB', 'protocolo', 'data', 'natureza', 'arquivo_da_exigencia')
    search_fields = ('NB', 'protocolo') # 'NB__requerente_titular__nome', 'NB__requerente_titular__cpf

admin.site.register(Exigencia, ExigenciaAdmin) # Registra o modelo Exigencia no admin do Django da Classe Exigencia e da configuração ExigenciaAdmin

class NaturezaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

admin.site.register(Natureza, NaturezaAdmin) # Registra o modelo Natureza no admin do Django da Classe Natureza e da configuração NaturezaAdmin

'''
class Recurso(models.Model):
    id = models.AutoField(primary_key=True) # ID do recurso
    NB = models.ForeignKey(Requerimento, on_delete=models.PROTECT, related_name='NB_recurso') # Relacionamento com o modelo Requerimento
    protocolo = models.CharField(max_length=20) # Número do protocolo do recurso
    data = models.DateField() # Data do recurso
    prazo_em_dias = 30 # Prazo para resposta do recurso
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='estado_recurso') # Estado do recurso Ex: Pendente, Concluído
    observacao = models.TextField() # Observações do recurso

    def __str__(self) -> str:
        return f'{self.requerimento.servico.nome}: {self.requerimento.requerente_titular.nome}, {self.requerimento.requerente_titular.cpf}, {self.requerimento.requerente_titular.data_nascimento}' # Retorna o nome do cliente e a data do recurso
    
class Exigencia(models.Model):
    id = models.AutoField(primary_key=True) # ID da exigência
    NB = models.ForeignKey(Requerimento, on_delete=models.PROTECT, related_name='NB_exigencia') # Relacionamento com o modelo Requerimento
    protocolo = models.CharField(max_length=20) # Número do protocolo da exigência
    data = models.DateField() # Data da exigência
    prazo_em_dias = 30 # Prazo para resposta da exigência
    natureza = models.ForeignKey('Natureza', on_delete=models.PROTECT, related_name='natureza_exigencia') # Natureza da exigência Ex: Documentação, Informação

class Natureza(models.Model):
    id = models.AutoField(primary_key=True) # ID da natureza
    nome = models.CharField(max_length=100) # Nome da natureza Ex: Documentação, Informação

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome da natureza
        '''