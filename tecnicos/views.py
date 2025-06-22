from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import TecnicoForm
from .models import Tecnico

@login_required
def cadastrar_tecnicos(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('tecnicos:listar_tecnicos')  # ajuste para sua url de listagem
            #enquanto não crio meu outro html
            return render(request, 'principal/home.html')
    else:
        form = TecnicoForm()
    return render(request, 'tecnicos/cadastrar_tecnicos.html', {'form': form})

@login_required
def listar_tecnicos(request):
    tecnicos = Tecnico.objects.all().order_by('-id')
    pesquisa = request.GET.get('pesquisa', '')

    if pesquisa:
        tecnicos = tecnicos.filter(
            Q(codigo__icontains=pesquisa) |
            Q(nome__icontains=pesquisa) |
            Q(email__icontains=pesquisa) |
            Q(cnpj_cpf__icontains=pesquisa) |
            Q(rg__icontains=pesquisa) |
            Q(telefone__icontains=pesquisa) |
            Q(celular__icontains=pesquisa)
        )

    paginator = Paginator(tecnicos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tecnicos/tecnicos.html', {'tecnico': tecnicos, 'page_obj': page_obj, 'pesquisa': pesquisa})

@login_required
def excluir_tecnico(request, tecnico_id):
    tecnicos = get_object_or_404(Tecnico, id=tecnico_id)
    tecnico.delete()
    return redirect('tecnicos:listar_tecnicos')

@login_required
def editar_tecnico(request, tecnico_id):
    tecnico = get_object_or_404(Tecnico, id=tecnico_id)
    if request.method == 'POST':
        form = TecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            form.save()
            return redirect('tecnicos:listar_tecnicos')
    else:
        form = TecnicoForm(instance=tecnico)
    return render(request, 'tecnicos/editar_Tecnico.html', {'form': form, 'tecnico': tecnico})

@login_required
def ver_tecnico(request, tecnico_id):
    tecnico = get_object_or_404(Tecnico, id=tecnico_id)
    return render(request, 'tecnicos/ver_tecnico.html', {'tecnico': tecnico})