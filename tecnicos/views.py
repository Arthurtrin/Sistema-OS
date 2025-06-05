from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TecnicoForm

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
