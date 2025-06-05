from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, EditarUsuarioForm
from .models import Perfil, Chave_Gerenciador
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import translation
from .add import gerar_chave_alfanumerica
from django.contrib.auth.models import User

def cadastro(request):
    translation.activate('pt-br')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            if form.cleaned_data['tipo_usuario'] in ['gerenciador', 'supervisor']:
                Chave_Gerenciador.objects.create(nome=usuario, chave=gerar_chave_alfanumerica())
            messages.success(request, 'Cadastro realizado com sucesso! Você já pode fazer login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

@login_required
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    perfil = get_object_or_404(Perfil, usuario=usuario)
    
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario, perfil=perfil)
        if form.is_valid():
            usuario = form.save()
            novo_tipo = form.cleaned_data['tipo_usuario']
            perfil.tipo = novo_tipo
            perfil.save()

            # Se for gerenciador ou supervisor, cria chave se não existir
            if novo_tipo in ['gerenciador', 'supervisor']:
                if not hasattr(usuario, 'chave_gerenciador'):
                    Chave_Gerenciador.objects.create(
                        nome=usuario,
                        chave=gerar_chave_alfanumerica()
                    )
            # Se for normal, exclui a chave se existir
            elif novo_tipo == 'normal':
                if hasattr(usuario, 'chave_gerenciador'):
                    usuario.chave_gerenciador.delete()

            messages.success(request, 'Usuário atualizado com sucesso.')
            return redirect('usuarios', usuario=request.user.username)
    else:
        form = EditarUsuarioForm(instance=usuario, perfil=perfil)
    
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
def excluir_usuario(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('usuarios', usuario=request.user.username)