from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from usuarios.models import Perfil


@login_required
def home(request):
    return render(request, 'principal/home.html')

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

            usuarios_perfis = [(perfil.usuario, perfil) for perfil in perfis]

            # Paginação: 10 itens por página
            paginator = Paginator(usuarios_perfis, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, 'principal/usuarios.html', {
                "page_obj": page_obj,
                "tipo_filtro": tipo_filtro,
                "pesquisa": pesquisa
            })
        else:
            return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    except Perfil.DoesNotExist:
        return HttpResponseForbidden("Perfil não encontrado.")