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
    
class LoginView(TemplateView):
    template_name = 'login.html'
    page_title = 'Login'

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super(LoginView, self).get_context_data(**kwargs)
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
    success_url = '/clientes/'
    

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = self.form_title
        return context

class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = 'form.html'
    form_class = ClienteModelForm
    page_title = 'Editando Cliente'
    form_title = 'Editando Cliente'
    form_title_identificador = None

    def get_success_url(self):
        return f'/cliente/{self.object.cpf}'
    
    def get_context_data(self, **kwargs):
        context = super(ClienteUpdateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f'{self.form_title}'
        context["form_title_identificador"] = f'CPF nº {self.object.cpf}'
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
    
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'delete.html'
    success_url = '/clientes/'
    page_title = 'Excluindo Cliente'
    form_title = 'Excluindo Cliente'
    tipo_objeto = 'o cliente'
    
    def get_context_data(self, **kwargs):
        context = super(ClienteDeleteView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f'{self.form_title}'
        context["form_title_identificador"] = f'de CPF nº {self.object.cpf}'
        context["tipo_objeto"] = self.tipo_objeto
        return context
    
class RequerimentoCreateView(CreateView):
    model = Requerimento
    template_name = 'form.html'
    form_class = RequerimentoModelForm
    page_title = 'Novo Requerimento'
    form_title = 'Novo Requerimento'
    form_title_identificador = None

    def get_initial(self):
        initial = super().get_initial()
        initial['requerente_titular'] = Cliente.objects.get(cpf=self.kwargs['cpf'])
        return initial
    
    def form_valid(self, form):
        form.instance.requerente_titular = Cliente.objects.get(cpf=self.kwargs['cpf'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return f'../cliente/{self.kwargs["cpf"]}'
    
    def get_context_data(self, **kwargs):
        context = super(RequerimentoCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f'{self.form_title}'
        context["form_title_identificador"] = f'CPF nº {self.kwargs["cpf"]}'
        return context
    
class RequerimentoUpdateView(UpdateView):
    model = Requerimento
    template_name = 'form.html'
    form_class = RequerimentoModelForm
    page_title = 'Editando Requerimento'
    form_title = 'Editando Requerimento'
    form_title_identificador = None

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        print(self.object.NB)
        return f'../{self.object.NB}'
    
    def get_context_data(self, **kwargs):
        context = super(RequerimentoUpdateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f'{self.form_title}'
        context["form_title_identificador"] = f'NB nº {self.object.NB} de {self.object.requerente_titular.nome}'
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

class RequerimentoDeleteView(DeleteView):
    model = Requerimento
    template_name = 'delete.html'
    success_url = '/clientes/'
    page_title = 'Excluindo Requerimento'
    form_title = 'Excluindo Requerimento'
    tipo_objeto = 'o requerimento'
    
    def get_context_data(self, **kwargs):
        context = super(RequerimentoDeleteView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f'{self.form_title}'
        context["form_title_identificador"] = f'de NB nº {self.object.NB}'
        context["tipo_objeto"] = self.tipo_objeto
        context["qtde_instancias_filhas"] = self.count_exigencias_and_recursos()
        return context
    
    def count_exigencias_and_recursos(self):
        total = self.object.NB_exigencia.count() + self.object.NB_recurso.count()
        return total

class IncidenteCreateView(CreateView):
    model = None
    template_name = 'form.html'
    form_class = None
    page_title = 'Novo Incidente'
    form_title = 'Novo Incidente'
    form_title_identificador = None

    def get_initial(self):
        initial = super().get_initial()
        initial['NB'] = Requerimento.objects.get(NB=self.kwargs['NB'])
        return initial

    def form_valid(self, form):
        form.instance.NB = Requerimento.objects.get(NB=self.kwargs['NB'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return f'../requerimento/{self.kwargs["NB"]}'
    
    def get_context_data(self, **kwargs):
        context = super(IncidenteCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = self.form_title
        context["form_title_identificador"] = f'NB nº {self.kwargs["NB"]}'
        return context
    
class ExigenciaCreateView(IncidenteCreateView):
    model = Exigencia
    form_class = ExigenciaModelForm
    page_title = 'Nova Exigência'
    form_title = 'Nova Exigência'

class IncidenteUpdateView(UpdateView):
    model = None
    template_name = 'form.html'
    form_class = None
    page_title = 'Editando'
    form_title = 'Editando'
    form_title_identificador = None

    def get_success_url(self):
        return f'../requerimento/{self.object.NB.NB}'
    
    def get_context_data(self, **kwargs):
        context = super(IncidenteUpdateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f'{self.form_title}'
        context["form_title_identificador"] = f'NB nº {self.object.NB.NB} de {self.object.NB.requerente_titular.nome}'
        return context

class ExigenciaUpdateView(IncidenteUpdateView):
    model = Exigencia
    form_class = ExigenciaModelForm
    slug_url_kwarg = 'slugfied_protocolo'
    page_title = 'Editando Exigência'
    form_title = 'Editando Exigência'

class RecursoCreateView(IncidenteCreateView):
    model = Recurso
    form_class = RecursoModelForm
    page_title = 'Novo Recurso'
    form_title = 'Novo Recurso'

class RecursoUpdateView(IncidenteUpdateView):
    model = Recurso
    form_class = RecursoModelForm
    page_title = 'Editando Recurso'
    form_title = 'Editando Recurso'

class IncidenteDeleteView(DeleteView):
    model = None
    template_name = 'delete.html'
    page_title = 'Excluindo'
    form_title = 'Excluindo'
    tipo_objeto = None
    
    def get_context_data(self, **kwargs):
        context = super(IncidenteDeleteView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f'{self.form_title}'
        context["form_title_identificador"] = f'de NB nº {self.object.NB.NB}'
        context["tipo_objeto"] = self.tipo_objeto
        return context
    
class ExigenciaDeleteView(IncidenteDeleteView):
    model = Exigencia
    page_title = 'Excluindo Exigência'
    form_title = 'Excluindo Exigência'
    tipo_objeto = 'a exigência'

class RecursoDeleteView(IncidenteDeleteView):
    model = Recurso
    page_title = 'Excluindo Recurso'
    form_title = 'Excluindo Recurso'
    tipo_objeto = 'o recurso'