from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from usuarios.models import Perfil, Chave_Gerenciador
from clientes.models import Cliente, Atividade, Segmento
from produtos.models import Grupo
from ordem_servico.models import OrdemServico, Status
from django.db.models.functions import Lower

@login_required
def home(request):
    pesquisa = request.GET.get('pesquisa', '')
    data_abertura = request.GET.get('data_abertura', '')

    ordens = OrdemServico.objects.all().order_by('-id')
    cliente = Cliente.objects.count()
    qtd_ordem = OrdemServico.objects.count()

    cancelada = Status.objects.annotate(nome_lower=Lower('nome')).filter(
    nome_lower__in=['cancelada', 'cancelado']
    ).first()
    finalizada = Status.objects.annotate(nome_lower=Lower('nome')).filter(
    nome_lower__in=['finalizada', 'finalizado']
    ).first()
    em_andamento = Status.objects.annotate(nome_lower=Lower('nome')).filter(nome_lower='em andamento').first()

    qtd_canceladas = OrdemServico.objects.filter(status=cancelada).count() if cancelada else 0
    qtd_finalizadas = OrdemServico.objects.filter(status=finalizada).count() if finalizada else 0
    qtd_andamento = OrdemServico.objects.filter(status=em_andamento).count() if em_andamento else 0
    if pesquisa:
        ordens = ordens.filter(
            Q(id__icontains=pesquisa) |
            Q(titulo__icontains=pesquisa) |
            Q(status__nome__icontains=pesquisa) |
            Q(n_cliente__nome_cliente__icontains=pesquisa) |
            Q(digitador__username__icontains=pesquisa) |
            Q(unidade__nome__icontains=pesquisa) |
            Q(segmento__nome__icontains=pesquisa) |
            Q(solicitante__icontains=pesquisa) |
            Q(municipio__icontains=pesquisa) | 
            Q(obra_nome__icontains=pesquisa)
        )
    
    if data_abertura:
        ordens = ordens.filter(data_abertura=data_abertura)

    return render(request, 'principal/home.html', {
        'pesquisa': pesquisa,
        'data_abertura': data_abertura,
        'clientes': cliente, 
        'ordens': ordens,
        'qtd_ordem':qtd_ordem,
        'qtd_canceladas': qtd_canceladas,
        'qtd_finalizadas': qtd_finalizadas,
        'qtd_andamento': qtd_andamento
        })

@login_required
def novo_template(request):
    return render(request, "principal/novo_template.html")

@login_required
def usuarios(request, usuario):
    try:
        perfil = Perfil.objects.get(usuario__username=usuario)
        if perfil.tipo == 'gerenciador':
            tipo_filtro = request.GET.get('tipo')
            pesquisa = request.GET.get('pesquisa')

            perfis = Perfil.objects.select_related('usuario')

            if tipo_filtro:
                perfis = perfis.filter(tipo=tipo_filtro)
            
            if pesquisa:
                perfis = perfis.filter(usuario__username__icontains=pesquisa)

            usuarios_perfis = []
            for perfil in perfis:
                try:
                    chave = Chave_Gerenciador.objects.get(nome=perfil.usuario)
                except Chave_Gerenciador.DoesNotExist:
                    chave = None
                usuarios_perfis.append((perfil.usuario, perfil, chave))

            # Paginação: 5 itens por página
            paginator = Paginator(usuarios_perfis, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'principal/usuarios.html', {
                "page_obj": page_obj,
                "tipo_filtro": tipo_filtro,
                "pesquisa": pesquisa
            })
        else:
            mensagem = 'Você não tem permissão para acessar esta página.'
            return render(request, 'principal/erro.html', {'mensagem': mensagem})
    except Perfil.DoesNotExist:
        mensagem = 'Perfil não encontrado'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})

@login_required
def configuracoes(request):
    return render(request, 'configuracoes/configuracoes.html')
