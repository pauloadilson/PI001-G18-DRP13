from django.shortcuts import render
from clientes.models import Cliente

# Create your views here.

def clientes_view(request):
    clientes = Cliente.objects.all()

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