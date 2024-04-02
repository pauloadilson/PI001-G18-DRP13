from django import forms

from clientes.models import Cliente, Estado, Servico, Requerimento

class ClienteForm(forms.Form):
    cpf = forms.CharField(max_length=11)
    nome = forms.CharField(max_length=100)
    data_nascimento = forms.DateField()
    telefone_whatsapp = forms.CharField(max_length=11,required=False)
    telefone = forms.CharField(max_length=11,required=False)

    def save(self):
        return Cliente.objects.create(**self.cleaned_data)

class RequerimentoForm(forms.Form):
    requerente_titular = forms.ModelChoiceField(Cliente.objects.all(), required=True)
    servico = forms.ModelChoiceField(Servico.objects.all(), required=True)
    NB = forms.CharField(max_length=20, required=False)
    requerente_dependentes = forms.TextInput() 
    tutor_curador = forms.ModelChoiceField(Cliente.objects.all(), required=False)
    instituidor = forms.ModelChoiceField(Cliente.objects.all(), required=False)
    data = forms.DateField() # Data do requerimento
    estado = forms.ModelChoiceField(Estado.objects.all(), required=True)
    observacao = forms.Textarea()


    def save(self):
        return Requerimento.objects.create(**self.cleaned_data)