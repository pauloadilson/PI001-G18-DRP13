from django import forms

from clientes.models import Cliente, Estado, Servico, Requerimento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class ClienteForm(forms.Form):
    cpf = forms.CharField(max_length=11, label='CPF')
    nome = forms.CharField(max_length=100, label='Nome')
    data_nascimento = forms.DateField(label='Data de Nascimento', widget=forms.SelectDateWidget())
    telefone_whatsapp = forms.CharField(max_length=11,required=False, label='WhatsApp')
    telefone = forms.CharField(max_length=11,required=False, label='Telefone')

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cpf', css_class='form-control'),
            Field('nome', css_class='form-control'),
            Field('data_nascimento', css_class='form-control', type='date'),
            Field('telefone_whatsapp', css_class='form-control'),
            Field('telefone', css_class='form-control'),
            Submit('submit', 'Cadastrar', css_class='btn btn-primary')
        )
    def save(self):
        return Cliente.objects.create(**self.cleaned_data)




class RequerimentoForm(forms.Form):
    requerente_titular = forms.ModelChoiceField(Cliente.objects.all(), required=True)
    servico = forms.ModelChoiceField(Servico.objects.all(), required=True)
    NB = forms.CharField(max_length=20, required=False)
    requerente_dependentes = forms.CharField(widget=forms.Textarea)
    tutor_curador = forms.ModelChoiceField(Cliente.objects.all(), required=False)
    instituidor = forms.ModelChoiceField(Cliente.objects.all(), required=False)
    data = forms.DateField(widget=forms.SelectDateWidget()) # Data do requerimento
    estado = forms.ModelChoiceField(Estado.objects.all(), required=True)
    observacao = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(RequerimentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('requerente_titular', css_class='form-control'),
            Field('servico', css_class='form-control'),
            Field('NB', css_class='form-control'),
            Field('requerente_dependentes', css_class='form-control'),
            Field('tutor_curador', css_class='form-control'),
            Field('instituidor', css_class='form-control'),
            Field('data', css_class='form-control', type='date'),
            Field('estado', css_class='form-control'),
            Field('observacao', css_class='form-control'),
            Submit('submit', 'Cadastrar', css_class='btn btn-primary')
        )

    def save(self):
        return Requerimento.objects.create(**self.cleaned_data)