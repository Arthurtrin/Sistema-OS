from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from usuarios.models import Perfil, Chave_Gerenciador
from .forms import ProdutoForm, MarcaForm, FabricanteForm, GrupoForm
from .models import Produto, Marca, Fabricante, Grupo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

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
    grupo = request.GET.get('grupo', '')
    fabricante = request.GET.get('fabricante', '')
    data_ultima_compra = request.GET.get('data_ultima_compra', '')

    produtos = Produto.objects.all().order_by('-id')

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

    if grupo:
        produtos = produtos.filter(grupo_id=grupo)

    if fabricante:
        produtos = produtos.filter(fabricante_id=fabricante)

    if data_ultima_compra:
        produtos = produtos.filter(data_ultima_compra=data_ultima_compra)

    paginator = Paginator(produtos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    grupos = Grupo.objects.all()
    fabricantes = Fabricante.objects.all()

    return render(request, 'produtos/produtos.html', {
        'page_obj': page_obj,
        'pesquisa': pesquisa,
        'situacao': situacao,
        'grupo': grupo,
        'fabricante': fabricante,
        'data_ultima_compra': data_ultima_compra,
        'grupos': grupos,
        'fabricantes': fabricantes,
        'Produto': Produto  # usado para acessar Produto.SITUACAO_CHOICES no template
    })

@login_required
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    return redirect('produtos:listar_produtos')

@login_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            produto = form.save()  # salva o cliente e guarda o objeto
            # registra a atividade do usuário
            #AtividadeUsuarioCliente.objects.create(
            #    usuario=request.user,
            #    cliente=cliente,
            #    descricao="Editou um cliente"
            #)
            return redirect('produtos:listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar_produto.html', {'form': form, 'produto': produto})

@login_required
def entrada_produto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigoEntrada')
        quantidade = request.POST.get('quantidadeEntrada')

        # Verifica se a quantidade é um número válido
        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError
        except (ValueError, TypeError):
            mensagem = 'A quantidade deve ser um número inteiro positivo.'
            return render(request, 'principal/erro.html', {'mensagem': mensagem})

        # Tenta buscar o produto
        try:
            produto = Produto.objects.get(codigo=codigo)
        except Produto.DoesNotExist:
            mensagem = 'Produto não encontrado.'
            return render(request, 'principal/erro.html', {'mensagem': mensagem})

        # Atualiza a quantidade do produto
        produto.quantidade += quantidade
        produto.save()

        messages.success(request, 'Entrada registrada com sucesso!')
        return redirect('home')

    return redirect('home')

def saida_produto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigoSaida')
        quantidade = request.POST.get('quantidadeSaida')

        # Verifica se a quantidade é um número inteiro positivo
        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError
        except (ValueError, TypeError):
            mensagem = 'A quantidade deve ser um número inteiro positivo.'
            return render(request, 'principal/erro.html', {'mensagem': mensagem})

        # Tenta buscar o produto
        try:
            produto = Produto.objects.get(codigo=codigo)
        except Produto.DoesNotExist:
            mensagem = 'Produto não encontrado.'
            return render(request, 'principal/erro.html', {'mensagem': mensagem})

        # Verifica se há estoque suficiente
        if produto.quantidade < quantidade:
            mensagem = 'Quantidade insuficiente em estoque.'
            return render(request, 'principal/erro.html', {'mensagem': mensagem})

        # Atualiza a quantidade do produto
        produto.quantidade -= quantidade
        produto.save()

        messages.success(request, 'Saída registrada com sucesso!')
        return redirect('home')

    return redirect('home')

@login_required
def fabricante_marca_grupo(request):
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
    grupo = Grupo.objects.all()

    return render(request, 'produtos/fabricante_marca_grupo.html', {
        "marcas": marca,
        "fabricantes": fabricante,
        "grupos":grupo
    })

@login_required
def ver_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'produtos/ver_produto.html', {'produto': produto})

@login_required
def cadastrar_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produtos:fabricante_marca_grupo')
    else:
        return redirect('produtos:fabricante_marca_grupo')

@login_required
def cadastrar_fabricante(request):
    if request.method == 'POST':
        form = FabricanteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('produtos:fabricante_marca_grupo') + '?aba=fabricantes')
    else:
        return redirect('produtos:fabricante_marca_grupo')

@login_required
def editar_marca(request, marca_id):
    marca = get_object_or_404(Marca, id=marca_id)
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            return redirect('produtos:fabricante_marca_grupo')  # Ajuste para a URL correta
    else:
        return redirect('produtos:fabricante_marca_grupo')

@login_required
def excluir_marca(request, marca_id):
    marca = get_object_or_404(Marca, id=marca_id)
    marca.delete()
    return redirect ('produtos:fabricante_marca_grupo')

@login_required
def editar_fabricante(request, fabricante_id):
    fabricante = get_object_or_404(Fabricante, id=fabricante_id)
    if request.method == 'POST':
        form = FabricanteForm(request.POST, instance=fabricante)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('produtos:fabricante_marca_grupo') + '?aba=fabricantes')
    else:
        return HttpResponseRedirect(reverse('produtos:fabricante_marca_grupo') + '?aba=fabricantes')

@login_required
def excluir_fabricante(request, fabricante_id):
    fabricante = get_object_or_404(Fabricante, id=fabricante_id)
    fabricante.delete()
    return HttpResponseRedirect(reverse('produtos:fabricante_marca_grupo') + '?aba=fabricantes')

@login_required
def cadastrar_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('produtos:fabricante_marca_grupo') + '?aba=grupos')
    else:
        return redirect('produtos:fabricante_marca_grupo')

@login_required
def editar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('produtos:fabricante_marca_grupo') + '?aba=grupos')
    else:
        return HttpResponseRedirect(reverse('produtos:fabricante_marca_grupo') + '?aba=grupos')

@login_required
def excluir_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    grupo.delete()
    return HttpResponseRedirect(reverse('produtos:fabricante_marca_grupo') + '?aba=grupos')