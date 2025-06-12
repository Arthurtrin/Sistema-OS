from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from usuarios.models import Perfil, Chave_Gerenciador
from .forms import ProdutoForm, MarcaForm, FabricanteForm
from .models import Produto, Marca, Fabricante
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'produtos/cadastrar_produto.html', {'form': form})
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar_produto.html', {'form': form})

@login_required
def listar_produtos(request):
    pesquisa = request.GET.get('pesquisa', '')
    situacao = request.GET.get('situacao', '')
    marca = request.GET.get('marca', '')
    fabricante = request.GET.get('fabricante', '')
    data_ultima_compra = request.GET.get('data_ultima_compra', '')

    produtos = Produto.objects.all()

    if pesquisa:
        produtos = produtos.filter(
            Q(codigo__icontains=pesquisa) |
            Q(nome__icontains=pesquisa) |
            Q(grupo__nome__icontains=pesquisa) |
            Q(situacao__icontains=pesquisa) |
            Q(fabricante__nome__icontains=pesquisa) |
            Q(marca__nome__icontains=pesquisa) |
            Q(ref_fabricante__icontains=pesquisa) |
            Q(cod_embalagem__icontains=pesquisa) |
            Q(cod_barra__icontains=pesquisa) | 
            Q(apresentacao__icontains=pesquisa) |
            Q(descricao__icontains=pesquisa)
        )

    if situacao:
        produtos = produtos.filter(situacao=situacao)

    if marca:
        produtos = produtos.filter(marca_id=marca)

    if fabricante:
        produtos = produtos.filter(fabricante_id=fabricante)

    if data_ultima_compra:
        produtos = produtos.filter(data_ultima_compra=data_ultima_compra)

    paginator = Paginator(produtos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    marcas = Marca.objects.all()
    fabricantes = Fabricante.objects.all()

    return render(request, 'produtos/produtos.html', {
        'page_obj': page_obj,
        'pesquisa': pesquisa,
        'situacao': situacao,
        'marca': marca,
        'fabricante': fabricante,
        'data_ultima_compra': data_ultima_compra,
        'marcas': marcas,
        'fabricantes': fabricantes,
        'Produto': Produto,  # usado para acessar Produto.SITUACAO_CHOICES no template
    })

@login_required
def fabricante_marca(request):
    usuario = request.user
    try:
        perfil = Perfil.objects.get(usuario=usuario)
    except Perfil.DoesNotExist:
        mensagem = 'Perfil não encontrado'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})

    if perfil.tipo not in ['gerenciador', 'supervisor']:
        mensagem = 'Você não tem permissão para acessar esta página.'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})

    marca = Marca.objects.all()
    fabricante = Fabricante.objects.all()
    
    return render(request, 'produtos/fabricante_marca.html', {
        "marcas": marca,
        "fabricantes": fabricante
    })

@login_required
def cadastrar_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produtos:fabricante_marca')
    else:
        return redirect('produtos:fabricante_marca')

@login_required
def cadastrar_fabricante(request):
    if request.method == 'POST':
        form = FabricanteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('produtos:fabricante_marca') + '?aba=fabricantes')
    else:
        return redirect('produtos:fabricante_marca')

@login_required
def editar_marca(request, marca_id):
    marca = get_object_or_404(Marca, id=marca_id)
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            return redirect('produtos:fabricante_marca')  # Ajuste para a URL correta
    else:
        return redirect('produtos:fabricante_marca')

@login_required
def excluir_marca(request, marca_id):
    marca = get_object_or_404(Marca, id=marca_id)
    marca.delete()
    return redirect ('produtos:fabricante_marca')

@login_required
def editar_fabricante(request, fabricante_id):
    fabricante = get_object_or_404(Fabricante, id=fabricante_id)
    if request.method == 'POST':
        form = FabricanteForm(request.POST, instance=fabricante)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('produtos:fabricante_marca') + '?aba=fabricantes')
    else:
        return HttpResponseRedirect(reverse('produtos:fabricante_marca') + '?aba=fabricantes')

@login_required
def excluir_fabricante(request, fabricante_id):
    fabricante = get_object_or_404(Fabricante, id=fabricante_id)
    fabricante.delete()
    return HttpResponseRedirect(reverse('produtos:fabricante_marca') + '?aba=fabricantes')
