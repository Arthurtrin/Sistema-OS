from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from .models import Empresa
from .forms import EmpresaForm
from django.contrib import messages
from principal import views

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