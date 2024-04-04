from django import forms

from clientes.models import Cliente, Estado, Servico, Requerimento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from clientes.models import Cliente


class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClienteModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cpf', css_class='form-control'),
            Field('nome', css_class='form-control'),
            Field('data_nascimento', css_class='form-control', type='date'),
            Field('telefone_whatsapp', css_class='form-control'),
            Field('telefone', css_class='form-control'),
            Submit('submit', 'Cadastrar', css_class='btn btn-primary')
        )

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        clientes = Cliente.objects.all() 
        if len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos')
        if cpf in [cliente.cpf for cliente in clientes]:
            raise forms.ValidationError('CPF já cadastrado')
        return cpf

    def save(self, commit=True):
        return super(ClienteModelForm, self).save(commit=commit)

    
class RequerimentoModelForm(forms.ModelForm):
    class Meta:
        model = Requerimento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RequerimentoModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('requerente_titular', css_class='form-control'),
            Field('servico', css_class='form-control'),
            Field('NB', css_class='form-control'),
            Field('requerente_dependentes', css_class='form-control'),
            Field('tutor_curador', css_class='form-control'),
            Field('instituidor', css_class='form-control'),
            Field('data', css_class='form-control', type='date', placeholder='dd/mm/aaaa'),
            Field('estado', css_class='form-control'),
            Field('observacao', css_class='form-control'),
            Submit('submit', 'Cadastrar', css_class='btn btn-primary')
        )

    def save(self, commit=True):
        return super(RequerimentoModelForm, self).save(commit=commit)