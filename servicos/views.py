from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from usuarios.models import Perfil, Chave_Gerenciador
from .forms import ServicoForm
from .models import Servico
from django.contrib import messages

from django.http import JsonResponse
from .models import Servico

def lista_de_servicos(request):
    servicos = Servico.objects.all().values("id", "nome", "preco")
    return JsonResponse(list(servicos), safe=False)

@login_required
def listar_servicos(request):
    servicos = Servico.objects.all().order_by('-id')
    return render(request, 'servicos/servicos.html', {"servicos":servicos})

@login_required
def cadastrar_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo Serviço criado com sucesso.')
            return redirect('servicos:listar_servicos')
    else:
        form = ServicoForm()
    return render(request, 'servicos/cadastrar_servico.html', {'form': form})
