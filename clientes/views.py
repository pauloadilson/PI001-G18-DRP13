from django.shortcuts import render, redirect
from clientes.models import Cliente
from clientes.form import ClienteForm, RequerimentoForm
# Create your views here.

def clientes_view(request):
    clientes = Cliente.objects.all() # .order_by('nome') '-nome' para ordem decrescente
    busca = request.GET.get('busca') # busca é o nome da chave de busca
    if request.method == 'POST':
        novo_cliente = ClienteForm(request.POST)
        if novo_cliente.is_valid():
            novo_cliente.save()
            return redirect('clientes')
        print(novo_cliente.data)
    elif busca:
        clientes = clientes.filter(cpf__icontains=busca)
        novo_cliente = ClienteForm()
    else:
        novo_cliente = ClienteForm()

    return render(
        request, 
        'clientes.html', 
        {
            'title': 'Clientes',
            'novo_cliente_form': novo_cliente,
            'clientes':clientes
        }
    )

def index(request):
    return render(
        request, 
        'index.html', 
        {
            'title': 'Página inicial',
        }
    )

def novo_requerimento_view(request):
    novo_requerimento = RequerimentoForm(request.POST or None)
    return render(
        request, 
        'novo_requerimento.html', 
        {
            'title': 'Novo Requerimento',
            'novo_requerimento_form': novo_requerimento
        }
    )