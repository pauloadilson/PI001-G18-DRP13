from django.db import models
from django.conf import settings

import os
from datetime import datetime

def path_and_rename(instance, filename):
    if isinstance(instance, Cliente):
        upload_to = 'arquivo_clientes/'
        pk = instance.cpf
    elif isinstance(instance, Requerimento):
        upload_to = 'arquivo_requerimentos/'
        pk = instance.NB
    elif isinstance(instance, Exigencia):
        upload_to = 'arquivo_exigencias/'
        pk = f'{instance.NB.NB}_{instance.protocolo}'
    elif isinstance(instance, Recurso):
        upload_to = 'arquivo_recursos/'
        pk = f'{instance.NB.NB}_{instance.protocolo}'
    else:
        upload_to = 'arquivos/'
    # get filename
    if pk:
        filename = f'{pk}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{filename}'
    else:
        # set filename as random string
        filename = f'{datetime.now().strftime('%Y%m%d%H%M%S')}.{filename}'
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key =True) # CPF é único para cada cliente Ex: 12345678900
    nome = models.CharField(max_length=100) # Nome do cliente Ex: João da Silva
    data_nascimento = models.DateField() # Data de nascimento do cliente Ex: 21-01-1990
    telefone_whatsapp = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888
    telefone = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888
    arquivo_do_cliente = models.FileField(upload_to=path_and_rename, blank=True, null=True) # Arquivos do cliente
    
    def __str__(self) -> str:
        return f'{self.cpf}, {self.nome}, {self.data_nascimento}, {self.telefone_whatsapp}, {self.telefone}'  # Retorna o nome do cliente e o CPF do cliente
    
class Servico(models.Model):
    id = models.AutoField(primary_key=True) # ID do serviço
    nome = models.CharField(max_length=100) # Nome do serviço Ex: Aposentadoria por idade, Aposentadoria por invalidez

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome do serviço

class Estado(models.Model):
    id = models.AutoField(primary_key=True) # ID do estado
    nome = models.CharField(max_length=100) # Nome do estado Ex: Em exigência, Em análise, Concluído

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome do estado
    
class Requerimento(models.Model):
    id = models.AutoField(primary_key=True) # ID do requerimento
    requerente_titular = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_titular_requerimento') # Relacionamento com o modelo Cliente
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name='servico_requerimento') # Serviço solicitado Ex: Aposentadoria por idade
    NB = models.SlugField(max_length=20, unique=True) # Número do benefício do cliente
    requerente_dependentes = models.TextField(blank=True, null=True) #.ManyToManyField(Cliente, related_name='cliente_dependente_requerimento', blank=True, null=True) # Relacionamento com o modelo Cliente
    tutor_curador = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_tutor_curador_requerimento', blank=True, null=True) # Relacionamento com o modelo Cliente
    instituidor = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_instituidor_requerimento', blank=True, null=True) # Relacionamento com o modelo Cliente
    data = models.DateField() # Data do requerimento
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='estado_requerimento') # Estado do requerimento Ex: Pendente, Concluído
    observacao = models.TextField() # Observações do requerimento
    arquivo_do_requerimento = models.FileField(upload_to=path_and_rename, blank=True, null=True) # Arquivos do requerimento

    def __str__(self) -> str:
        return f'{self.servico.nome}: {self.requerente_titular.nome}, {self.requerente_titular.cpf}, {self.requerente_titular.data_nascimento}' # Retorna o nome do cliente e a data do requerimento

class Natureza(models.Model):
    id = models.AutoField(primary_key=True) # ID da natureza
    nome = models.CharField(max_length=100) # Nome da natureza Ex: Documentação, Informação

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome da natureza
    
class Exigencia(models.Model):
    id = models.AutoField(primary_key=True) # ID da exigência
    NB = models.ForeignKey(Requerimento, on_delete=models.PROTECT, related_name='NB_exigencia') # Relacionamento com o modelo Requerimento
    protocolo = models.CharField(max_length=20) # Número do protocolo da exigência
    data = models.DateField() # Data da exigência
    prazo_em_dias = 30 # Prazo para resposta da exigência
    natureza = models.ForeignKey(Natureza, on_delete=models.PROTECT, related_name='natureza_exigencia') # Natureza da exigência Ex: Documentação, Informação
    arquivo_da_exigencia = models.FileField(upload_to=path_and_rename, blank=True, null=True) # Arquivos da exigência
    
    def __str__(self) -> str:
        return f'{self.NB.servico.nome}: {self.NB.requerente_titular.nome}, {self.NB.requerente_titular.cpf}, {self.NB.requerente_titular.data_nascimento}'

class Recurso(models.Model):
    id = models.AutoField(primary_key=True) # ID do recurso
    NB = models.ForeignKey(Requerimento, on_delete=models.PROTECT, related_name='NB_recurso') # Relacionamento com o modelo Requerimento
    protocolo = models.CharField(max_length=20) # Número do protocolo do recurso
    data = models.DateField() # Data do recurso
    prazo_em_dias = 30 # Prazo para resposta do recurso
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='estado_recurso') # Estado do recurso Ex: Pendente, Concluído
    observacao = models.TextField() # Observações do recurso
    arquivo_do_recurso = models.FileField(upload_to=path_and_rename, blank=True, null=True) # Arquivos do recurso

    def __str__(self) -> str:
        return f'{self.NB.servico.nome}: {self.NB.requerente_titular.nome}, {self.NB.requerente_titular.cpf}, {self.NB.requerente_titular.data_nascimento}' # Retorna o nome do cliente e a data do recurso
    