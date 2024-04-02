from django.shortcuts import render
from clientes.models import Cliente
# Create your views here.

def clientes_view(request):
    clientes = Cliente.objects.all() # .order_by('nome') '-nome' para ordem decrescente
    busca = request.GET.get('busca') # busca é o nome da chave de busca
    if busca:
        clientes = clientes.filter(cpf__icontains=busca).order_by('nome')

    return render(
        request, 
        'clientes.html', 
        {
            'title': 'Clientes',
            'clientes':clientes
        }
    )

def index(request):
    return render(
        request, 
        'index.html', 
        {
            'title': 'Home',
        }
    )