from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmpresaForm
from django.contrib import messages
from .models import FormaPagamento

# Create your views here.
def principal(request):
    return render(request, 'financeiro/principal.html')

def cadastrar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        print("cehgou aqui")
        if form.is_valid():
            print("veio para ca")
            form.save() 
            messages.success(request, 'Nova empresa cadastrada com sucesso.')
            return redirect('financeiro:principal')
    else:
        form = EmpresaForm()
    return render(request, 'financeiro/cadastrar_empresa.html', {'form': form})

def forma_pg(request):
    formas = FormaPagamento.objects.all()
    return render(request, 'financeiro/formas_pagamento.html', {'formas':formas})

def cadastrar_forma_pagamento(request):
    forma = request.POST.get('forma')
    if forma:
        FormaPagamento.objects.create(forma=forma)
    return redirect('financeiro:forma_pg')

def excluir_forma_pagamento(request, id):
    forma = get_object_or_404(FormaPagamento, id=id)
    forma.delete()
    return redirect('financeiro:forma_pg')

def editar_forma_pagamento(request, id):
    forma = get_object_or_404(FormaPagamento, id=id)
    forma.forma = request.POST.get('forma')
    forma.save()
    return redirect('financeiro:forma_pg')
