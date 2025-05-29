from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ClienteForm
from .models import Cliente

def cadastrar_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes:listar_clientes')  # ou outra view
    else:
        form = ClienteForm()

    return render(request, 'clientes/cadastrar_clientes.html', {'form': form})

def listar_clientes(request):
    pesquisa = request.GET.get('pesquisa', '')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    clientes = Cliente.objects.all()

    if pesquisa:
        clientes = clientes.filter(
            Q(codigo__icontains=pesquisa) |
            Q(nome_cliente__icontains=pesquisa) |
            Q(nome_fantasia__icontains=pesquisa) |
            Q(email1__icontains=pesquisa) |
            Q(email2__icontains=pesquisa) |
            Q(email3__icontains=pesquisa) |
            Q(cnpj_cpf__icontains=pesquisa) |
            Q(telefone1__icontains=pesquisa) |
            Q(telefone2__icontains=pesquisa) |
            Q(celular1__icontains=pesquisa) | 
            Q(celular2__icontains=pesquisa) |
            Q(inscricao_estadual__icontains=pesquisa) |
            Q(inscricao_municipal__icontains=pesquisa)
        )

    if data_inicio:
        clientes = clientes.filter(data_inclusao__date__gte=data_inicio)

    if data_fim:
        clientes = clientes.filter(data_inclusao__date__lte=data_fim)

    paginator = Paginator(clientes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'clientes/clientes.html', {
        'page_obj': page_obj,
        'pesquisa': pesquisa,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    })

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes:listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_clientes.html', {'form': form, 'cliente': cliente})

def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('clientes:listar_clientes')

def ver_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'clientes/ver_cliente.html', {'cliente': cliente})