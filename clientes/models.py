from django.db import models
from django.conf import settings

class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key =True) # CPF é único para cada cliente Ex: 12345678900
    nome = models.CharField(max_length=100) # Nome do cliente Ex: João da Silva
    data_nascimento = models.DateField() # Data de nascimento do cliente Ex: 21-01-1990
    telefone_whatsapp = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888
    telefone = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888

    def __str__(self) -> str:
        return f'{self.nome}, {self.data_nascimento}, {self.cpf}'  # Retorna o nome do cliente e o CPF do cliente
    
class Estado(models.Model):
    id = models.AutoField(primary_key=True) # ID do estado
    nome = models.CharField(max_length=100) # Nome do estado Ex: Em exigência, Em análise, Concluído

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome do estado

class Servico(models.Model):
    id = models.AutoField(primary_key=True) # ID do serviço
    nome = models.CharField(max_length=100) # Nome do serviço Ex: Aposentadoria por idade, Aposentadoria por invalidez

    def __str__(self) -> str:
        return f'{self.nome}' # Retorna o nome do serviço

class Requerimento(models.Model):
    id = models.AutoField(primary_key=True) # ID do requerimento
    NB = models.CharField(max_length=20, blank=True, null=True) # Número do benefício do cliente
    requerente_titular = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_titular_requerimento') # Relacionamento com o modelo Cliente
    requerente_dependentes = models.TextField(blank=True, null=True) #.ManyToManyField(Cliente, related_name='cliente_dependente_requerimento', blank=True, null=True) # Relacionamento com o modelo Cliente
    tutor_curador = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_tutor_curador_requerimento', blank=True, null=True) # Relacionamento com o modelo Cliente
    instituidor = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_instituidor_requerimento', blank=True, null=True) # Relacionamento com o modelo Cliente
    data = models.DateField() # Data do requerimento
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='estado_requerimento') # Estado do requerimento Ex: Pendente, Concluído
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name='servico_requerimento') # Serviço solicitado Ex: Aposentadoria por idade
    observacao = models.TextField() # Observações do requerimento

    def __str__(self) -> str:
        return f'{self.servico.nome}: {self.requerente_titular.nome}, {self.requerente_titular.cpf}, {self.requerente_titular.data_nascimento}' # Retorna o nome do cliente e a data do requerimento