from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def clientes_view(request):
    return HttpResponse('Meus clientes')