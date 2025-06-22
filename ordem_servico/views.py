from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ordem_servico.forms import OrdemServicoForm 
from .models import OrdemServico

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
