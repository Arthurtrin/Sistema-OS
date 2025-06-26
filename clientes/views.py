from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ClienteForm, SegmentoForm, AtividadeForm
from .models import Cliente, Segmento, Atividade
from atividades.models import AtividadeUsuarioCliente
from django.contrib.auth.decorators import login_required
from usuarios.models import Perfil, Chave_Gerenciador
from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required
def cadastrar_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()  # salva o cliente e guarda o objeto
            # registra a atividade do usuário
            AtividadeUsuarioCliente.objects.create(
                usuario=request.user,
                cliente=cliente,
                descricao="Cadastrou um novo cliente"
            )
            return redirect('clientes:listar_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/cadastrar_clientes.html', {'form': form})

@login_required
def listar_clientes(request):
    pesquisa = request.GET.get('pesquisa', '')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    clientes = Cliente.objects.all().order_by('-id')

    if pesquisa:
        clientes = clientes.filter(
            Q(codigo__icontains=pesquisa) |
            Q(nome_cliente__icontains=pesquisa) |
            Q(nome_fantasia__icontains=pesquisa) |
            Q(email1__icontains=pesquisa) |
            Q(email2__icontains=pesquisa) |
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

    qtd_clientes = Cliente.objects.count()
    qtd_segmentos = Segmento.objects.count()
    qtd_atividades = Atividade.objects.count()
    qtd_estados = Cliente.objects.values('estado_real').distinct().count()
    return render(request, 'clientes/clientes.html', {
        'page_obj': page_obj,
        'pesquisa': pesquisa,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        "qtd_clientes": qtd_clientes,
        "qtd_segmentos": qtd_segmentos,
        "qtd_atividades": qtd_atividades,
        "qtd_estados": qtd_estados
    })

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()  # salva o cliente e guarda o objeto
            # registra a atividade do usuário
            AtividadeUsuarioCliente.objects.create(
                usuario=request.user,
                cliente=cliente,
                descricao="Editou um cliente"
            )
            return redirect('clientes:listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_clientes.html', {'form': form, 'cliente': cliente})

@login_required
def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('clientes:listar_clientes')

@login_required
def ver_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'clientes/ver_cliente.html', {'cliente': cliente})

@login_required
def segmentos_atividades(request):
    usuario = request.user
    try:
        perfil = Perfil.objects.get(usuario=usuario)
    except Perfil.DoesNotExist:
        mensagem = 'Perfil não encontrado'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})

    if perfil.tipo not in ['gerenciador', 'supervisor']:
        mensagem = 'Você não tem permissão para acessar esta página.'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})

    segmento = Segmento.objects.all()
    atividade = Atividade.objects.all()
    
    return render(request, 'clientes/segmentos_atividade.html', {
        "atividades": atividade,
        "segmentos": segmento
    })

@login_required
def editar_segmento(request, seg_id):
    segmento = get_object_or_404(Segmento, id=seg_id)
    if request.method == 'POST':
        form = SegmentoForm(request.POST, instance=segmento)
        if form.is_valid():
            form.save()
            return redirect('clientes:segmentos_atividades')  # Ajuste para a URL correta
    else:
        form = SegmentoForm(instance=segmento)
    return render(request, 'clientes/editar_segmento.html', {'form': form, 'segmento': segmento})

@login_required
def excluir_segmento(request, seg_id):
    segmento = get_object_or_404(Segmento, id=seg_id)
    segmento.delete()
    return redirect ('clientes:segmentos_atividades')  

@login_required
def editar_atividade(request, atv_id):
    atividade = get_object_or_404(Atividade, id=atv_id)
    if request.method == 'POST':
        form = AtividadeForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clientes:segmentos_atividades') + '?aba=atividades')
    else:
        form = AtividadeForm(instance=atividade)
    return render(request, 'clientes/editar_atividade.html', {'form': form, 'atividade': atividade})

@login_required
def excluir_atividade(request, atv_id):
    atividade = get_object_or_404(Atividade, id=atv_id)
    atividade.delete()
    return HttpResponseRedirect(reverse('clientes:segmentos_atividades') + '?aba=atividades')

@login_required
def cadastrar_segmento(request):
    if request.method == 'POST':
        form = SegmentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes:segmentos_atividades')  # Ajuste para a URL correta
    else:
        form = SegmentoForm()
    return render(request, 'clientes/cadastrar_segmento.html', {'form': form})

@login_required
def cadastrar_atividade(request):
    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clientes:segmentos_atividades') + '?aba=atividades')
    else:
        form = AtividadeForm()
    return render(request, 'clientes/cadastrar_atividade.html', {'form': form})