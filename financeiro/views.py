from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmpresaForm, FornecedorForm
from django.contrib import messages
from .models import FormaPagamento, Empresa, Fornecedor

# Create your views here.
def principal(request):
    return render(request, 'financeiro/principal.html')

def empresas(request):
    empresas = Empresa.objects.all().order_by('-id')
    return render(request, 'financeiro/empresas.html', {'empresas':empresas})

def fornecedores(request):
    fornecedores = Fornecedor.objects.all().order_by('-id')
    return render(request, 'financeiro/fornecedores.html', {'fornecedores':fornecedores})

def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():  
            form.save()
            messages.success(request, 'Novo fornecedor cadastrado com sucesso.')
            return redirect('financeiro:fornecedores')
    else:
        form = FornecedorForm()
    return render(request, 'financeiro/cadastrar_fornecedores.html', {'form': form}) 

def cadastrar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():  
            form.save() 
            messages.success(request, 'Nova empresa cadastrada com sucesso.')
            return redirect('financeiro:empresas')
    else:
        form = EmpresaForm()
    return render(request, 'financeiro/cadastrar_empresa.html', {'form': form})

def editar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa atualizada com sucesso.')
            return redirect('financeiro:empresas')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'financeiro/editar_empresa.html', {'form': form, 'empresa': empresa})

def excluir_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    empresa.delete()
    messages.success(request, 'Empresa excluída com sucesso.')
    return redirect('financeiro:empresas')




def receitas(request):
    pass

def cadastrar_forma_pagamento(request):
    if request.method == 'POST':
        forma = request.POST.get('forma')
        if forma:
            FormaPagamento.objects.create(forma=forma)
        return redirect('financeiro:cadastrar_forma_pagamento')
    else:
        formas = FormaPagamento.objects.all()
    return render(request, 'financeiro/formas_pagamento.html', {'formas':formas})

def excluir_forma_pagamento(request, id):
    forma = get_object_or_404(FormaPagamento, id=id)
    forma.delete()
    return redirect('financeiro:cadastrar_forma_pagamento')

def editar_forma_pagamento(request, id):
    forma = get_object_or_404(FormaPagamento, id=id)
    forma.forma = request.POST.get('forma')
    forma.save()
    return redirect('financeiro:cadastrar_forma_pagamento')
