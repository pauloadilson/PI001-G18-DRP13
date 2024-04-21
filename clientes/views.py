from django.shortcuts import render, redirect
from clientes.models import Cliente, Requerimento
from clientes.form import ClienteModelForm, RequerimentoModelForm, RecursoModelForm, ExigenciaModelForm
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
# Create your views here.

def index(request):
    return render(
        request, 
        'index.html', 
        {
            'title': 'Página inicial',
        }
    )

class ClientesView(View):
    def get(self, request):
        clientes = Cliente.objects.all() 
        busca = request.GET.get('busca') 
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

    def post(self, request):
        novo_cliente = ClienteModelForm(request.POST)
        if novo_cliente.is_valid():
            novo_cliente.save()
            return redirect('clientes')
        return render(
            request, 
            'novo_cliente.html', 
            {
                'title': 'Novo Cliente',
                'form_name': 'Novo Cliente',
                'novo_cliente_form': novo_cliente
            }
        )


class NovoClienteView(View):
    def get(self, request):
        novo_cliente = ClienteModelForm()
        return render(
            request, 
            'novo_cliente.html', 
            {
                'title': 'Novo Cliente',
                'form_name': 'Novo Cliente',
                'novo_cliente_form': novo_cliente
            }
        )

    def post(self, request):
        novo_cliente = ClienteModelForm(request.POST)
        if novo_cliente.is_valid():
            novo_cliente.save()
            cliente_id = novo_cliente.cleaned_data.get('cpf')
            return redirect(f'../cliente/?cpf={cliente_id}')
        return render(
            request, 
            'novo_cliente.html', 
            {
                'title': 'Novo Cliente',
                'form_name': 'Novo Cliente',
                'novo_cliente_form': novo_cliente
            }
        )

def cliente_view(request):
    clientes = Cliente.objects.all() # .order_by('nome') '-nome' para ordem decrescente
    cliente_id = request.GET.get('cpf') # busca é o nome da chave de busca
    requerimentos = Requerimento.objects.all()
    cliente = clientes.filter(cpf__icontains=cliente_id)[0]
    requerimentos_cliente = requerimentos.filter(requerente_titular__cpf__icontains=cliente_id)


    return render(
        request, 
        'cliente.html', 
        {
            'title': f'Cliente {cliente_id}',
            'cliente':cliente,
            'requerimentos_cliente':requerimentos_cliente,
        }
    )

def novo_requerimento_view(request):
    cliente_id = request.GET.get('cpf') # busca é o nome da chave de busca
    
    if request.method == 'POST':
        novo_requerimento = RequerimentoModelForm(request.POST or None)
        if novo_requerimento.is_valid():
            novo_requerimento.save()
            return redirect(f'../cliente/?cpf={cliente_id}')
    else:
        novo_requerimento = RequerimentoModelForm()

    return render(
        request, 
        'novo_requerimento.html', 
        {
            'title': 'Novo Requerimento',
            'form_name': 'Novo Requerimento',
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
    exigencias = requerimento.NB_exigencia.all()
    recursos = requerimento.NB_recurso.all()
        
    return render(
        request, 
        'requerimento.html', 
        {
            'title': 'Requerimentos',
            'requerimento':requerimento,
            'cliente':cliente,
            'exigencias': exigencias,
            'recursos': recursos,
        }
    )

def nova_exigencia_view(request):
    NB = request.GET.get('NB')
    if request.method == 'POST':
        nova_exigencia = ExigenciaModelForm(request.POST)
        if nova_exigencia.is_valid():
            nova_exigencia.save()
            return redirect(f'../requerimento/?NB={NB}')
    else:
        nova_exigencia = ExigenciaModelForm()

    return render(
        request, 
        'nova_exigencia.html', 
        {
            'title': 'Nova Exigência',
            'form_name': 'Nova Exigência',
            'nova_exigencia_form': nova_exigencia
        }
    )

def novo_recurso_view(request):
    NB = request.GET.get('NB')
    if request.method == 'POST':
        novo_recurso = RecursoModelForm(request.POST)
        if novo_recurso.is_valid():
            novo_recurso.save()
            return redirect(f'../requerimento/?NB={NB}')
    else:
        novo_recurso = RecursoModelForm()

    return render(
        request, 
        'novo_recurso.html', 
        {
            'title': 'Novo Recurso',
            'form_name': 'Novo Recurso',
            'novo_recurso_form': novo_recurso
        }
    )