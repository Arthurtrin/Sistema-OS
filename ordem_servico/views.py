from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ordem_servico.forms import OrdemServicoForm 
from .models import OrdemServico, Status, Unidade, Segmento
from .forms import SegmentoForm, StatusForm, UnidadeForm
from usuarios.models import Perfil, Chave_Gerenciador
from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required
def criar_os(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ordem_servico:criar_os')
    else:
        form = OrdemServicoForm()
    return render(request, 'ordem_servico/criar_os.html', {'form': form})

@login_required
def definicao(request):
    usuario = request.user
    try:
        perfil = Perfil.objects.get(usuario=usuario)
    except Perfil.DoesNotExist:
        mensagem = 'Perfil não encontrado'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})

    if perfil.tipo not in ['gerenciador', 'supervisor']:
        mensagem = 'Você não tem permissão para acessar esta página.'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})

    segmentos = Segmento.objects.all()
    unidades = Unidade.objects.all()
    status_list = Status.objects.all()
    return render(request, "ordem_servico/segmentos_status_unidades.html",{
        "segmentos": segmentos,
        "unidades": unidades,
        "status_list": status_list
    })

# Segmentos
@login_required
def cadastrar_segmento(request):
    if request.method == 'POST':
        form = SegmentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ordem_servico:definicao')  # Ajuste para a URL correta
    else:
        form = SegmentoForm()
    return redirect('ordem_servico:definicao')

@login_required
def editar_segmento(request, segmento_id):
    segmento = get_object_or_404(Segmento, id=segmento_id)
    if request.method == 'POST':
        form = SegmentoForm(request.POST, instance=segmento)
        if form.is_valid():
            form.save()
            return redirect('ordem_servico:definicao')  # Ajuste para a URL correta
    else:
        return redirect('ordem_servico:definicao')

@login_required
def excluir_segmento(request, segmento_id):
    segmento = get_object_or_404(Segmento, id=segmento_id)
    segmento.delete()
    return redirect('ordem_servico:definicao')

# Unidades
@login_required
def cadastrar_unidade(request):
    if request.method == 'POST':
        form = UnidadeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=unidades') 
    else:
        form = SegmentoForm()
    return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=unidades')

@login_required
def editar_unidade(request, unidade_id):
    unidade = get_object_or_404(Unidade, id=unidade_id)
    if request.method == 'POST':
        form = SegmentoForm(request.POST, instance=unidade)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=unidades')
    else:
        return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=unidades')

@login_required
def excluir_unidade(request, unidade_id):
    unidade = get_object_or_404(Unidade, id=unidade_id)
    unidade.delete()
    return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=unidades')

# Status
@login_required
def cadastrar_status(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=status') 
    else:
        form = SegmentoForm()
    return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=status')

@login_required
def editar_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    if request.method == 'POST':
        form = SegmentoForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=status')
    else:
        return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=status')

@login_required
def excluir_status(request, status_id):
    status = get_object_or_404(Status, id=status_id)
    status.delete()
    return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=status')