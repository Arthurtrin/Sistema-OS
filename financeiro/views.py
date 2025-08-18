from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmpresaForm, FornecedorForm, ContasReceberForm
from django.contrib import messages
from .models import FormaPagamento, Empresa, Fornecedor, LocalCobranca, ContasReceber

# TELA PRINCIPAL
def principal(request):
    return render(request, 'financeiro/principal.html')

#EMPRESA
def empresas(request):
    empresas = Empresa.objects.all().order_by('-id')
    return render(request, 'financeiro/empresa/empresas.html', {'empresas':empresas})

def cadastrar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():  
            form.save() 
            messages.success(request, 'Nova empresa cadastrada com sucesso.')
            return redirect('financeiro:empresas')
    else:
        form = EmpresaForm()
    return render(request, 'financeiro/empresa/cadastrar_empresa.html', {'form': form})

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
    return render(request, 'financeiro/empresa/editar_empresa.html', {'form': form, 'empresa': empresa})

def excluir_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    empresa.delete()
    messages.success(request, 'Empresa excluída com sucesso.')
    return redirect('financeiro:empresas')

#FORNECEDORES
def fornecedores(request):
    fornecedores = Fornecedor.objects.all().order_by('-id')
    return render(request, 'financeiro/fornecedor/fornecedores.html', {'fornecedores':fornecedores})

def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():  
            form.save()
            messages.success(request, 'Novo fornecedor cadastrado com sucesso.')
            return redirect('financeiro:fornecedores')
    else:
        form = FornecedorForm()
    return render(request, 'financeiro/fornecedor/cadastrar_fornecedores.html', {'form': form}) 

def editar_fornecedores(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa atualizada com sucesso.')
            return redirect('financeiro:fornecedores')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'financeiro/fornecedor/editar_fornecedores.html', {'form': form, 'fornecedor': fornecedor})

def excluir_fornecedores(request, id):
    fornecedor = get_object_or_404(Fornecedor, id=id)
    fornecedor.delete()
    messages.success(request, 'Fornecedor excluído com sucesso.')
    return redirect('financeiro:fornecedores')

#FORMAS DE PAGAMENTO
def cadastrar_forma_pagamento(request):
    if request.method == 'POST':
        forma = request.POST.get('forma')
        if forma:
            FormaPagamento.objects.create(forma=forma)
        return redirect('financeiro:cadastrar_forma_pagamento')
    else:
        formas = FormaPagamento.objects.all()
    return render(request, 'financeiro/formapagamento/formas_pagamento.html', {'formas':formas})

def excluir_forma_pagamento(request, id):
    forma = get_object_or_404(FormaPagamento, id=id)
    forma.delete()
    return redirect('financeiro:cadastrar_forma_pagamento')

def editar_forma_pagamento(request, id):
    forma = get_object_or_404(FormaPagamento, id=id)
    forma.forma = request.POST.get('forma')
    forma.save()
    return redirect('financeiro:cadastrar_forma_pagamento')

#LOCAIS DE COBRANÇA
def locais_cobranca(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            LocalCobranca.objects.create(nome=nome)
        return redirect('financeiro:locais_cobranca')
    else:
        locais = LocalCobranca.objects.all()
    return render(request, 'financeiro/localcobranca/locais_cobrancas.html', {'locais':locais})

def excluir_locais_cobranca(request, id):
    local = get_object_or_404(LocalCobranca, id=id)
    local.delete()
    return redirect('financeiro:locais_cobranca')

def editar_locais_cobranca(request, id):
    local = get_object_or_404(LocalCobranca, id=id)
    local.nome = request.POST.get('nome')
    local.save()
    return redirect('financeiro:locais_cobranca')

def receitas(request):
    receitas = ContasReceber.objects.all().order_by('-id')
    return render(request, 'financeiro/receitas/receitas.html', {'receitas':receitas})

def cadastrar_receita(request):
    if request.method == 'POST':
        form = ContasReceberForm(request.POST)
        if form.is_valid():  
            form.save()
            messages.success(request, 'Nova receita cadastrada com sucesso.')
            return redirect('financeiro:fornecedores')
    else:
        form = ContasReceberForm()
    return render(request, 'financeiro/receitas/cadastrar_receita.html', {'form': form})

def editar_receita(request, id):
    pass

def excluir_receita(request, id):
    conta = get_object_or_404(ContasReceber, id=id)
    conta.delete()
    messages.success(request, 'Receita excluída com sucesso.')
    return redirect('financeiro:receitas')