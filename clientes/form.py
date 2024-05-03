from django import forms

from clientes.models import Cliente, Requerimento, Recurso, Exigencia
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Button, HTML
from crispy_forms.bootstrap import FormActions

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
            Field('data_nascimento', css_class='form-control date_picker', placeholder='dd/mm/aaaa'),
            Field('telefone_whatsapp', css_class='form-control'),
            Field('telefone', css_class='form-control'),
            Field('arquivo_do_cliente', css_class='form-control'),
            FormActions(
                Submit('submit', 'Salvar', css_class='btn btn-primary'),
                Button('button', 'Voltar', css_class='btn btn-secondary', onclick='window.history.back()'),
            )
        )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        clientes = Cliente.objects.all() 
        if len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos')
        if (isinstance(self.instance, Cliente) and Cliente.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists()):
            raise forms.ValidationError('CPF já cadastrado')
        #if cpf in [cliente.cpf for cliente in clientes]:
        #    raise forms.ValidationError('CPF já cadastrado')
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
            Field('requerente_titular', css_class='form-control', type='hidden'),
            Field('servico', css_class='form-control'),
            Field('NB', css_class='form-control'),
            Field('slugfied_NB', css_class='form-control'),
            Field('requerente_dependentes', css_class='form-control'),
            Field('tutor_curador', css_class='form-control'),
            Field('instituidor', css_class='form-control'),
            Field('data', css_class='form-control date_picker', placeholder='dd/mm/aaaa'),
            Field('estado', css_class='form-control'),
            Field('observacao', css_class='form-control'),
            Field('arquivo_do_requerimento', css_class='form-control'),
            FormActions(
                Submit('submit', 'Salvar', css_class='btn btn-primary'),
                Button('button', 'Voltar', css_class='btn btn-secondary', onclick='window.history.back()'),
            )
        )

    def save(self, commit=True):
        return super(RequerimentoModelForm, self).save(commit=commit)

class ExigenciaModelForm(forms.ModelForm):
    class Meta:
        model = Exigencia
        fields = ('NB', 'protocolo', 'data', 'natureza', 'arquivo_da_exigencia')

    def __init__(self, *args, **kwargs):
        super(ExigenciaModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('NB', css_class='form-control', type='hidden'),
            Field('protocolo', css_class='form-control'),
            Field('data', css_class='form-control date_picker', placeholder='dd/mm/aaaa'),
            Field('natureza', css_class='form-control'),
            Field('estado', css_class='form-control'),
            Field('arquivo_da_exigencia', css_class='form-control'),
            FormActions(
                Submit('submit', 'Salvar', css_class='btn btn-primary'),
                Button('button', 'Voltar', css_class='btn btn-secondary', onclick='window.history.back()'),
            )
        )

    def save(self, commit=True):
        return super(ExigenciaModelForm, self).save(commit=commit)
    
class RecursoModelForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = ('NB', 'protocolo', 'data', 'estado', 'observacao', 'arquivo_do_recurso')

    def __init__(self, *args, **kwargs):
        super(RecursoModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('NB', css_class='form-control', type='hidden'),
            Field('protocolo', css_class='form-control'),
            Field('data', css_class='form-control date_picker', placeholder='dd/mm/aaaa'),
            Field('estado', css_class='form-control'),
            Field('observacao', css_class='form-control'),
            Field('arquivo_do_recurso', css_class='form-control'),
            FormActions(
                Submit('submit', 'Salvar', css_class='btn btn-primary'),
                Button('button', 'Voltar', css_class='btn btn-secondary', onclick='window.history.back()'),
            )
        )

    def save(self, commit=True):
        return super(RecursoModelForm, self).save(commit=commit)
    

