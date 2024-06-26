from django.contrib.auth.decorators import login_required
from django.db.models.base import Model as Model
from django.http import Http404
from django.utils.decorators import method_decorator
from clientes.models import Cliente, Requerimento, Exigencia, Recurso
from clientes.form import (
    ClienteModelForm,
    RequerimentoModelForm,
    RecursoModelForm,
    ExigenciaModelForm,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.shortcuts import redirect
from itertools import chain


class IndexView(TemplateView):
    template_name = "index.html"
    page_title = "Página inicial"

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super(IndexView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class ClientesListView(ListView):
    model = Cliente
    template_name = "clientes.html"
    context_object_name = "clientes"
    page_title = "Clientes"
    ordering = ["nome"]
    paginate_by = 10

    def get_queryset(self):
        clientes = super().get_queryset().filter(is_deleted=False)
        busca = self.request.GET.get("busca")
        if busca:
            clientes = clientes.filter(cpf__icontains=busca)
        return clientes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context

@method_decorator(login_required(login_url='login'), name='dispatch')
class ClienteCreateView(CreateView):

    model = Cliente
    template_name = "form.html"
    form_class = ClienteModelForm
    page_title = "Novo Cliente"
    form_title = "Novo Cliente"
    success_url = "/clientes/"

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = self.form_title
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = "form.html"
    form_class = ClienteModelForm
    page_title = "Editando Cliente"
    form_title = "Editando Cliente"
    form_title_identificador = None

    def get_success_url(self):
        return reverse_lazy("cliente", kwargs={"pk": self.object.cpf})

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f"{self.form_title}"
        context["form_title_identificador"] = f"CPF nº {self.object.cpf}"
        return context
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj


@method_decorator(login_required(login_url='login'), name='dispatch')
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = "cliente.html"
    context_object_name = "cliente"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(ClienteDetailView, self).get_context_data(**kwargs)
        cliente_id = self.object.cpf
        page_title = f"Cliente {cliente_id}"
        requerimentos_cliente = Requerimento.objects.filter(is_deleted=False).filter(
            requerente_titular__cpf__icontains=cliente_id
        )
        qtde_instancias_filhas = requerimentos_cliente.count()

        context["page_title"] = page_title
        context["requerimentos_cliente"] = requerimentos_cliente
        context["qtde_instancias_filhas"] = qtde_instancias_filhas

        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "delete.html"
    success_url = "/clientes/"
    page_title = "Excluindo Cliente"
    form_title = "Excluindo Cliente"
    tipo_objeto = "o cliente"

    def get_context_data(self, **kwargs):
        context = super(ClienteDeleteView, self).get_context_data(**kwargs)
        cliente_id = self.object.cpf
        requerimentos_cliente = Requerimento.objects.filter(is_deleted=False).filter(
            requerente_titular__cpf__icontains=cliente_id
        )
        qtde_instancias_filhas = requerimentos_cliente.count()

        context["page_title"] = self.page_title
        context["form_title"] = f"{self.form_title}"
        context["form_title_identificador"] = f"de CPF nº {self.object.cpf}"
        context["tipo_objeto"] = self.tipo_objeto
        context["qtde_instancias_filhas"] = qtde_instancias_filhas
        context["result_list"] = requerimentos_cliente
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class RequerimentoCreateView(CreateView):
    model = Requerimento
    template_name = "form.html"
    form_class = RequerimentoModelForm
    page_title = "Novo Requerimento"
    form_title = "Novo Requerimento"
    form_title_identificador = None

    def get_initial(self):
        initial = super().get_initial()
        initial["requerente_titular"] = Cliente.objects.filter(is_deleted=False).get(cpf=self.kwargs["cpf"])
        return initial

    def form_valid(self, form):
        form.instance.requerente_titular = Cliente.objects.filter(is_deleted=False).get(cpf=self.kwargs["cpf"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("requerimento", kwargs={"NB": self.object.NB})

    def get_context_data(self, **kwargs):
        context = super(RequerimentoCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f"{self.form_title}"
        context["form_title_identificador"] = f'CPF nº {self.kwargs["cpf"]}'
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class RequerimentoDetailView(DetailView):
    model = Requerimento
    slug_field = "NB"
    slug_url_kwarg = "NB"
    template_name = "requerimento.html"
    context_object_name = "requerimento"
    page_title = "Requerimento"
    paginate_by = 10

    cliente_id = None

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj

    def get_context_data(self, **kwargs):
        context = super(RequerimentoDetailView, self).get_context_data(**kwargs)

        cliente_id = self.object.requerente_titular.cpf
        cliente = Cliente.objects.filter(is_deleted=False).filter(cpf__icontains=cliente_id)[
            0
        ]  # .order_by('nome') '-nome' para ordem decrescente
        exigencias_requerimento = self.object.NB_exigencia.filter(is_deleted=False).filter(NB__NB=self.object.NB)
        recursos_requerimento = self.object.NB_recurso.filter(is_deleted=False).filter(NB__NB=self.object.NB)
        qtde_instancias_filhas = (
            exigencias_requerimento.count() + recursos_requerimento.count()
        )

        context["page_title"] = self.page_title
        context["cliente"] = cliente
        context["exigencias_requerimento"] = exigencias_requerimento
        context["recursos_requerimento"] = recursos_requerimento
        context["qtde_instancias_filhas"] = qtde_instancias_filhas
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class RequerimentoUpdateView(UpdateView):
    model = Requerimento
    template_name = "form.html"
    form_class = RequerimentoModelForm
    page_title = "Editando Requerimento"
    form_title = "Editando Requerimento"
    form_title_identificador = None
    slug_field = "NB"
    slug_url_kwarg = "NB"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj
    
    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("requerimento", kwargs={"NB": self.object.NB})

    def get_context_data(self, **kwargs):
        context = super(RequerimentoUpdateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f"{self.form_title}"
        context["form_title_identificador"] = (
            f"NB nº {self.object.NB} de {self.object.requerente_titular.nome}"
        )
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class RequerimentoDeleteView(DeleteView):
    model = Requerimento
    template_name = "delete.html"
    success_url = "clientes"
    page_title = "Excluindo Requerimento"
    form_title = "Excluindo Requerimento"
    tipo_objeto = "o requerimento"
    slug_field = "NB"
    slug_url_kwarg = "NB"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj

    def get_context_data(self, **kwargs):
        context = super(RequerimentoDeleteView, self).get_context_data(**kwargs)

        numero_NB = self.object.NB
        exigencias_requerimento = Exigencia.objects.filter(is_deleted=False).filter(NB__NB=numero_NB)
        recursos_requerimento = Recurso.objects.filter(is_deleted=False).filter(NB__NB=numero_NB)
        qtde_instancias_filhas = (
            exigencias_requerimento.count() + recursos_requerimento.count()
        )
        result_list = list(chain(exigencias_requerimento, recursos_requerimento))

        context["page_title"] = self.page_title
        context["form_title"] = f"{self.form_title}"
        context["form_title_identificador"] = f"de NB nº {self.object.NB}"
        context["tipo_objeto"] = self.tipo_objeto
        context["qtde_instancias_filhas"] = qtde_instancias_filhas
        context["exigencias_requerimento"] = exigencias_requerimento
        context["recursos_requerimento"] = recursos_requerimento
        context["result_list"] = result_list
        return context
    
    def get_success_url(self):
        return reverse_lazy("cliente", kwargs={"pk": self.object.requerente_titular.cpf})


@method_decorator(login_required(login_url='login'), name='dispatch')
class IncidenteCreateView(CreateView):
    model = None
    template_name = "form.html"
    form_class = None
    page_title = "Novo Incidente"
    form_title = "Novo Incidente"
    form_title_identificador = None

    def get_initial(self):
        initial = super().get_initial()
        initial["NB"] = Requerimento.objects.get(NB=self.kwargs["NB"])
        return initial

    def form_valid(self, form):
        form.instance.NB = Requerimento.objects.get(NB=self.kwargs["NB"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("requerimento", kwargs={"NB": self.kwargs["NB"]})

    def get_context_data(self, **kwargs):
        context = super(IncidenteCreateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = self.form_title
        context["form_title_identificador"] = f'NB nº {self.kwargs["NB"]}'
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class ExigenciaCreateView(IncidenteCreateView):
    model = Exigencia
    form_class = ExigenciaModelForm
    page_title = "Nova Exigência"
    form_title = "Nova Exigência"
    # success_url = "/requerimentos/"


@method_decorator(login_required(login_url='login'), name='dispatch')
class IncidenteUpdateView(UpdateView):
    model = None
    template_name = "form.html"
    form_class = None
    page_title = "Editando"
    form_title = "Editando"
    form_title_identificador = None

    def get_success_url(self):
        return reverse_lazy("requerimento", kwargs={"NB": self.kwargs["NB"]})

    def get_context_data(self, **kwargs):
        context = super(IncidenteUpdateView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f"{self.form_title}"
        context["form_title_identificador"] = (
            f"NB nº {self.object.NB.NB} de {self.object.NB.requerente_titular.nome}"
        )
        return context
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class ExigenciaUpdateView(IncidenteUpdateView):
    model = Exigencia
    form_class = ExigenciaModelForm
    page_title = "Editando Exigência"
    form_title = "Editando Exigência"


@method_decorator(login_required(login_url='login'), name='dispatch')
class RecursoCreateView(IncidenteCreateView):
    model = Recurso
    form_class = RecursoModelForm
    page_title = "Novo Recurso"
    form_title = "Novo Recurso"


@method_decorator(login_required(login_url='login'), name='dispatch')
class RecursoUpdateView(IncidenteUpdateView):
    model = Recurso
    form_class = RecursoModelForm
    page_title = "Editando Recurso"
    form_title = "Editando Recurso"


@method_decorator(login_required(login_url='login'), name='dispatch')
class IncidenteDeleteView(DeleteView):
    model = None
    template_name = "delete.html"
    page_title = "Excluindo"
    form_title = "Excluindo"
    tipo_objeto = None

    def get_context_data(self, **kwargs):
        context = super(IncidenteDeleteView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = f"{self.form_title}"
        context["form_title_identificador"] = f"de NB nº {self.object.NB.NB}"
        context["tipo_objeto"] = self.tipo_objeto
        context["qtde_instancias_filhas"] = 0
        return context

    def get_success_url(self):
        return reverse_lazy("requerimento", kwargs={"NB": self.object.NB.NB})
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_deleted:
            raise Http404("Requerimento não encontrado")
        return obj
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class ExigenciaDeleteView(IncidenteDeleteView):
    model = Exigencia
    page_title = "Excluindo Exigência"
    form_title = "Excluindo Exigência"
    tipo_objeto = "a exigência"


@method_decorator(login_required(login_url='login'), name='dispatch')
class RecursoDeleteView(IncidenteDeleteView):
    model = Recurso
    page_title = "Excluindo Recurso"
    form_title = "Excluindo Recurso"
    tipo_objeto = "o recurso"


@method_decorator(login_required(login_url='login'), name='dispatch')
class PrazoView(TemplateView):

    # Redireciona o usuário não logado
    login_url = "/login/"
    redirect_field_name = "redirect_to"
 
    template_name = "prazo.html"
    page_title = "Prazo"

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super(PrazoView, self).get_context_data(**kwargs)
        ultimos_30_dias = datetime.now() - timedelta(days=30)
        
        exigencias_nao_crumpridas = (
            Exigencia.objects.all()
            .filter(is_deleted=False).select_related("NB")
            .select_related("NB__requerente_titular")
            .exclude(estado__nome="Cumprido")
        )
        exigencias_futuras = exigencias_nao_crumpridas.filter(data_final_prazo__gt=datetime.now())
        exigencias_vencidas = exigencias_nao_crumpridas.filter(
            data_final_prazo__range=(ultimos_30_dias, datetime.now())
        )
        existem_exigencias_futuras = exigencias_futuras.exists()
        existem_exigencias_vencidas = exigencias_vencidas.exists()
        
        recursos_nao_cumpridos = (
            Recurso.objects.all()
            .filter(is_deleted=False).select_related("NB")
            .select_related("NB__requerente_titular")
            .exclude(estado__nome="Cumprido")
        )
        recursos_futuros = recursos_nao_cumpridos.filter(data_final_prazo__gt=datetime.now())
        recursos_vencidos = recursos_nao_cumpridos.filter(
            data_final_prazo__range=(ultimos_30_dias, datetime.now())
        )
        existem_recursos_futuros = recursos_futuros.exists()
        existem_recursos_vencidos = recursos_vencidos.exists()

        context["page_title"] = self.page_title
        context["exigencias_futuras"] = exigencias_futuras
        context["exigencias_vencidas"] = exigencias_vencidas
        context["existem_exigencias_futuras"] = existem_exigencias_futuras
        context["existem_exigencias_vencidas"] = existem_exigencias_vencidas
        context["recursos_futuros"] = recursos_futuros
        context["recursos_vencidos"] = recursos_vencidos
        context["existem_recursos_futuros"] = existem_recursos_futuros
        context["existem_recursos_vencidos"] = existem_recursos_vencidos
        return context

class Custom404View(TemplateView):
    template_name = "404.html"
    page_title = "Página não encontrada"

    def get_context_data(self, **kwargs):
        context = super(Custom404View, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        return context
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response