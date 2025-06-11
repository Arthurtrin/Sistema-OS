from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProdutoForm
from .models import Produto, Marca, Fabricante

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
