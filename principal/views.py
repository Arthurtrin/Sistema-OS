from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from usuarios.models import Perfil, Chave_Gerenciador
from clientes.models import Cliente, Atividade, Segmento
from produtos.models import Grupo

@login_required
def home(request):
    cliente = Cliente.objects.count()
    return render(request, 'principal/home.html', {"clientes": cliente})

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
def ordem_servico(request):
    return render(request, 'principal/ordem_servico.html')

@login_required
def criar_os(request):
    grupos = Grupo.objects.all()  # ou como você busca seus dados
    labels = ['Digitador', 'Unidade', 'Segmento']
    obra_campos = ['Início', 'Término', 'Nº ART', 'Nome']
    return render(request, 'ordem_servico/criar_os.html', {
        'grupos': grupos,
        'grupo': '',  # ou o ID do grupo selecionado
        'labels': labels,
        'obra_campos': obra_campos,
    })

@login_required
def configuracoes(request):
    return render(request, 'principal/configuracoes.html')
