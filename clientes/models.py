from django.db import models

class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key =True) # CPF é único para cada cliente Ex: 12345678900
    nome = models.CharField(max_length=100) # Nome do cliente Ex: João da Silva
    data_nascimento = models.DateField() # Data de nascimento do cliente Ex: 21-01-1990
    telefone_whatsapp = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888
    telefone = models.CharField(max_length=11, blank=True, null=True) # Telefone do cliente Ex: 81999998888
