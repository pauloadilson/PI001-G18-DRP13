from django.shortcuts import render, redirect
from clientes.models import Cliente, Requerimento
from clientes.form import ClienteModelForm, RequerimentoModelForm
# Create your views here.

def clientes_view(request):
    clientes = Cliente.objects.all() # .order_by('nome') '-nome' para ordem decrescente
    busca = request.GET.get('busca') # busca é o nome da chave de busca
    if request.method == 'POST':
        novo_cliente = ClienteModelForm(request.POST)
        if novo_cliente.is_valid():
            novo_cliente.save()
            return redirect('clientes')
        print(novo_cliente.data)
    elif busca:
        clientes = clientes.filter(cpf__icontains=busca)
        novo_cliente = ClienteModelForm()
    else:
        novo_cliente = ClienteModelForm()

    return render(
        request, 
        'clientes.html', 
        {
            'title': 'Clientes',
            'novo_cliente_form': novo_cliente,
            'clientes':clientes
        }
    )
def cliente_view(request):
    clientes = Cliente.objects.all() # .order_by('nome') '-nome' para ordem decrescente
    cliente_id = request.GET.get('cpf') # busca é o nome da chave de busca
#    cliente_id = '35307319860' # busca é o nome da chave de busca
    requerimentos = Requerimento.objects.all()
    cliente = clientes.filter(cpf__icontains=cliente_id)[0]
    requerimentos_cliente = requerimentos.filter(requerente_titular__cpf__icontains=cliente_id)

    return render(
        request, 
        'cliente.html', 
        {
            'title': f'Cliente {cliente_id}',
            'cliente':cliente,
            'requerimentos_cliente':requerimentos_cliente
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
    novo_requerimento = RequerimentoModelForm(request.POST or None)
    return render(
        request, 
        'novo_requerimento.html', 
        {
            'title': 'Novo Requerimento',
            'novo_requerimento_form': novo_requerimento
        }
    )