from clientes.models import Cliente, Requerimento, Exigencia, Recurso
from clientes.form import ClienteModelForm, RequerimentoModelForm, RecursoModelForm, ExigenciaModelForm
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    page_title = 'Página inicial'

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

class ClientesListView(ListView):
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'clientes'
    page_title = 'Clientes'
    ordering = ['nome']
    paginate_by = 10

    def get_queryset(self):
        clientes = super().get_queryset()
        busca = self.request.GET.get('busca') 
        if busca:
            clientes = clientes.filter(cpf__icontains=busca)
        return clientes
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'form.html'
    form_class = ClienteModelForm
    page_title = 'Novo Cliente'
    form_title = 'Novo Cliente'
    cliente_id = form_class.clean_cpf
    success_url = f'../cliente/?cpf={cliente_id}'

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = self.form_title
        return context

class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'cliente.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        cliente_id = self.object.cpf
        page_title = f'Cliente {cliente_id}'
        requerimentos = Requerimento.objects.all()
        requerimentos_cliente = requerimentos.filter(requerente_titular__cpf__icontains=cliente_id)
        context["page_title"] = page_title
        context["requerimentos_cliente"] = requerimentos_cliente
        return context
    
class RequerimentoCreateView(CreateView):
    model = Requerimento
    template_name = 'form.html'
    form_class = RequerimentoModelForm
    page_title = 'Novo Requerimento'
    form_title = 'Novo Requerimento'

    def get_context_data(self, **kwargs):
        context = super(RequerimentoCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = self.form_title
        return context
    
class RequerimentoDetailView(DetailView):
    model = Requerimento
    slug_field = 'NB'
    slug_url_kwarg = 'NB'
    template_name = 'requerimento.html'
    context_object_name = 'requerimento'
    page_title = 'Requerimento'
    paginate_by = 10

    cliente_id = None
    
    def get_context_data(self, **kwargs):
        context = super(RequerimentoDetailView, self).get_context_data(**kwargs)
        cliente_id = self.object.requerente_titular.cpf
        clientes = Cliente.objects.all() # .order_by('nome') '-nome' para ordem decrescente
        cliente = clientes.filter(cpf__icontains=cliente_id)[0]
        exigencias = self.object.NB_exigencia.all()
        recursos = self.object.NB_recurso.all()
        context["page_title"] = self.page_title
        context["cliente"] = cliente
        context["exigencias"] = exigencias
        context["recursos"] = recursos
        return context
    
class ExigenciaCreateView(CreateView):
    model = Exigencia
    template_name = 'form.html'
    form_class = ExigenciaModelForm
    page_title = 'Nova Exigência'
    form_title = 'Nova Exigência'
    
    def get_context_data(self, **kwargs):
        context = super(ExigenciaCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = self.form_title
        return context
class RecursoCreateView(CreateView):
    model = Recurso
    template_name = 'form.html'
    form_class = RecursoModelForm
    page_title = 'Novo Recurso'
    form_title = 'Novo Recurso'
    
    def get_context_data(self, **kwargs):
        context = super(RecursoCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = self.form_title
        return context