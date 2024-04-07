from django.shortcuts import render, redirect
from clientes.models import Cliente, Requerimento
from clientes.form import ClienteModelForm, RequerimentoModelForm, RecursoModelForm, ExigenciaForm, ExigenciaModelForm
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
    novo_requerimento = RequerimentoModelForm(request.POST or None)


    return render(
        request, 
        'cliente.html', 
        {
            'title': f'Cliente {cliente_id}',
            'cliente':cliente,
            'requerimentos_cliente':requerimentos_cliente,
            'novo_requerimento_form': novo_requerimento

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

def requerimento_view(request):
    requerimentos = Requerimento.objects.all() # .order_by('nome') '-nome' para ordem decrescente
    nb = request.GET.get('NB') # busca é o nome da chave de busca
    requerimento = requerimentos.filter(NB__icontains=nb)[0]
    requerimento_titular_id = requerimento.requerente_titular.cpf
    clientes = Cliente.objects.all() # .order_by('nome') '-nome' para ordem decrescente
    cliente = clientes.filter(cpf__icontains=requerimento_titular_id)[0]

    nova_exigencia = ExigenciaForm(request.POST or None)
    novo_recurso = RecursoModelForm(request.POST or None)

    exigencias = requerimento.NB_exigencia.all()
    recursos = requerimento.NB_recurso.all()

    exigencias = [{
                'NB': requerimento.NB,
                'protocolo': '20210058745',
                'data': '01/07/2021',
                'natureza': 'Falta documentação'
            }]
    recursos =         [{
                'NB': requerimento.NB,
                'protocolo': '20214578587',
                'data': '10/10/2021',
                'estado': 'Concluído',
                'observacao': 'Grupo de recursos do INSS',
            },
            {
                'NB': requerimento.NB,
                'protocolo': '20227896554',
                'data': '02/02/2022',
                'estado': 'Em análise',
                'observacao': 'Conselho de recurso do INSS',
                'natureza': 'Documentação'
            }]
            
        
    return render(
        request, 
        'requerimento.html', 
        {
            'title': 'Requerimentos',
            'requerimento':requerimento,
            'cliente':cliente,
            'exigencias': exigencias,
            'recursos': recursos,
            'nova_exigencia_form': nova_exigencia,
            'novo_recurso_form': novo_recurso
        }
    )