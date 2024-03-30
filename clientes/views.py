from django.shortcuts import render

# Create your views here.

def clientes_view(request):
    return render(
        request, 
        'clientes.html', 
        {
            'clientes': [{
                'cpf': 35307319860, 
                'nome': 'João da Silva', 
                'data_nascimento': '1990-01-21', 
                'telefone_whatsapp': 81999998888, 
                'telefone': 81999998888, 
            },
            {
                'cpf': 21841043885, 
                'nome': 'Roberto da Silva', 
                'data_nascimento': '1981-02-23', 
                'telefone_whatsapp': 81999998888, 
                'telefone': 81999998888, 
            }],
        }
    )
            