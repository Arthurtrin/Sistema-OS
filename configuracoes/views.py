from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from .models import Empresa
from .forms import EmpresaForm
from django.contrib import messages
from principal import views
from usuarios.models import Perfil, Chave_Gerenciador

class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'configuracoes/configuracao_empresa.html'

    def get_object(self, queryset=None):
        # Garante que sempre vai pegar a única empresa cadastrada
        return Empresa.objects.first()

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Dados da Empresa salvos com sucesso!')
        return redirect('configuracoes')

@login_required
def usuario(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        perfil = None

    try:
        chave_gerenciador = request.user.chave_gerenciador
    except Chave_Gerenciador.DoesNotExist:
        chave_gerenciador = None

    return render(request, 'configuracoes/usuario.html', {
        'perfil': perfil,
        'chave_gerenciador': chave_gerenciador,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)

    # Apenas o próprio usuário pode editar seu perfil
    if request.user != usuario:
        messages.error(request, 'Você não tem permissão para editar este perfil.')
        return redirect('configuracoes:usuario')

    if request.method == 'POST':
        novo_username = request.POST.get('username', '').strip()
        novo_email = request.POST.get('email', '').strip()

        # Verifica se o novo nome de usuário já existe em outro usuário
        if User.objects.filter(username=novo_username).exclude(id=usuario.id).exists():
            messages.error(request, 'Já existe um usuário com esse nome.')
            return redirect('configuracoes:usuario')

        usuario.username = novo_username
        usuario.email = novo_email
        usuario.save()

        messages.success(request, 'Dados atualizados com sucesso.')
        return redirect('configuracoes:usuario')

    return redirect('configuracoes:usuario')
