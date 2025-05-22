from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Perfil, Chave_Gerenciador
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import translation
from .add import gerar_chave_alfanumerica

def cadastro(request):
    translation.activate('pt-br')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            if form.cleaned_data['tipo_usuario'] == 'gerenciador':
                Chave_Gerenciador.objects.create(nome=usuario.username, chave=gerar_chave_alfanumerica())
            messages.success(request, 'Cadastro realizado com sucesso! Você já pode fazer login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})
