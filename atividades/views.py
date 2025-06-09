from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import AtividadeUsuarioCliente
from django.core.paginator import Paginator

# Create your views here.
@login_required
def ver_atividades(request):
    atividade = AtividadeUsuarioCliente.objects.all()
    paginator = Paginator(atividade, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "atividades/atividades.html", {'atividade' : atividade, 'page_obj': page_obj,})