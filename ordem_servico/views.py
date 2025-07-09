from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrdemServico, Status, Unidade, Segmento, ProdutoOrdemServico
from .forms import SegmentoForm, StatusForm, UnidadeForm, OrdemServicoForm, ProdutoOrdemServicoForm
from produtos.models import Produto
from usuarios.models import Perfil, Chave_Gerenciador
from configuracoes.models import Empresa
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from django.contrib import messages
from django.db.models import ProtectedError

@login_required
def criar_os(request):
    ProdutoFormSet = modelformset_factory(
        ProdutoOrdemServico,
        form=ProdutoOrdemServicoForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        os_form = OrdemServicoForm(request.POST, request.FILES)
        produto_formset = ProdutoFormSet(request.POST, prefix='form')

        if os_form.is_valid() and produto_formset.is_valid():
            # ETAPA 1 – Verifica se tem estoque suficiente antes de salvar
            erro_estoque = False
            for i, form in enumerate(produto_formset.forms):
                acao = request.POST.get(f'form-{i}-acao', 'mantem')
                baixa = request.POST.get(f'form-{i}-baixa', 'nao')

                if acao == 'mantem' and baixa == 'sim':
                    produto = form.cleaned_data.get('produto')
                    quantidade = form.cleaned_data.get('quantidade')

                    if produto and quantidade is not None:
                        try:
                            produto_db = Produto.objects.get(id=produto.id)
                            if produto_db.quantidade < quantidade:
                                erro_estoque = True
                                messages.error(request, f'Estoque insuficiente para o produto "{produto_db.nome}". Quantidade disponível: {produto_db.quantidade}, Solicitada: {quantidade}')
                        except Produto.DoesNotExist:
                            erro_estoque = True
                            messages.error(request, f'Produto não encontrado no banco de dados.')
            
            if erro_estoque:
                # NÃO salva nada se houver erro de estoque
                return render(request, 'ordem_servico/criar_os.html', {
                    'form': os_form,
                    'produto_formset': produto_formset
                })

            # ETAPA 2 – Salvar a ordem e os produtos com baixa validada
            ordem_servico = os_form.save()

            for i, form in enumerate(produto_formset.forms):
                acao = request.POST.get(f'form-{i}-acao', 'mantem')
                baixa = request.POST.get(f'form-{i}-baixa', 'nao')

                if acao == 'delete':
                    print(f'[IGNORADO] Produto marcado como delete: {form.cleaned_data.get("produto")}')
                    continue

                if acao == 'mantem' and form.has_changed():
                    produto_os = form.save(commit=False)
                    produto_os.ordem_servico = ordem_servico
                    produto_os.baixa = (baixa == 'sim')
                    print(produto_os.baixa)
                    produto_os.save()

                    print(f'Produto salvo: {produto_os.produto}, Quantidade: {produto_os.quantidade}, Baixa: {produto_os.baixa}')

                    if baixa == 'sim':
                        produto = Produto.objects.get(id=produto_os.produto.id)
                        print(produto)
                        verif = int(produto.quantidade) - int(produto_os.quantidade)
                        print(produto.quantidade, " ", produto_os.quantidade, " ", verif)
                        produto.quantidade = verif
                        produto.save()
                        print(f'Estoque atualizado: {produto.nome}, nova quantidade: {produto.quantidade}')

                    
            messages.success(request, 'Nova ordem de serviço criada com sucesso.')
            return redirect('ordem_servico:criar_os')
        else:
            print("Erros no formulário de produto:", produto_formset.errors)
    else:
        os_form = OrdemServicoForm()
        produto_formset = ProdutoFormSet(queryset=ProdutoOrdemServico.objects.none(), prefix='form')

    return render(request, 'ordem_servico/criar_os.html', {
        'form': os_form,
        'produto_formset': produto_formset
    })

@login_required
def editar_os(request, os_id):
    ordem_servico = get_object_or_404(OrdemServico, id=os_id)

    ProdutoFormSet = modelformset_factory(
        ProdutoOrdemServico,
        form=ProdutoOrdemServicoForm,
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        os_form = OrdemServicoForm(request.POST, request.FILES, instance=ordem_servico)
        produto_formset = ProdutoFormSet(
            request.POST,
            queryset=ProdutoOrdemServico.objects.filter(ordem_servico=ordem_servico),
            prefix='form'
        )

        if os_form.is_valid() and produto_formset.is_valid():
            erro_estoque = False
            estoque_temporario = {}

            # Copia dos produtos antigos ANTES de qualquer alteração
            produtos_antigos = ProdutoOrdemServico.objects.filter(ordem_servico=ordem_servico)
            produtos_antigos_cop = list(produtos_antigos)
            for p in produtos_antigos:
                print(p.produto.nome, p.baixa)
            # Passo 1 – Repor estoque se houve baixa anterior e agora não há mais

            for i, antigo in enumerate(produtos_antigos_cop):
                baixa_anterior = antigo.baixa
                produto = antigo.produto
                baixa_atual_str = request.POST.get(f'form-{i}-baixa', 'nao')
                baixa_atual = baixa_atual_str == 'sim'
                print(baixa_anterior, " ", baixa_atual)
                if baixa_anterior and not baixa_atual and produto:
                    produto.quantidade += antigo.quantidade
                    produto.save()
                    
                    print(f"[REPOSIÇÃO] {produto.nome} -> estoque restaurado: {produto.quantidade}")

                if produto:
                    estoque_temporario[produto.id] = produto.quantidade

            # Passo 2 – Valida novo estoque antes de subtrair
            for i, form in enumerate(produto_formset.forms):
                acao = request.POST.get(f'form-{i}-acao', 'mantem')
                baixa = request.POST.get(f'form-{i}-baixa', 'nao')

                if acao == 'mantem' and baixa == 'sim':
                    produto = form.cleaned_data.get('produto')
                    quantidade = form.cleaned_data.get('quantidade')

                    if produto and quantidade is not None:
                        estoque_disponivel = estoque_temporario.get(produto.id, produto.quantidade)
                        if estoque_disponivel < quantidade:
                            erro_estoque = True
                            messages.error(
                                request,
                                f'Estoque insuficiente para o produto \"{produto.nome}\". '
                                f'Disponível: {estoque_disponivel}, Solicitado: {quantidade}'
                            )

            if erro_estoque:
                return render(request, 'ordem_servico/editar_os.html', {
                    'form': os_form,
                    'produto_formset': produto_formset,
                    'ordem_servico': ordem_servico
                })

            # Passo 3 – Salva OS e produtos
            os_form.save()
            produtos_antigos.delete()

            for i, form in enumerate(produto_formset.forms):
                acao = request.POST.get(f'form-{i}-acao', 'mantem')
                baixa = request.POST.get(f'form-{i}-baixa', 'nao')
                baixa_atual = baixa == 'sim'  # converte para bool

                if acao == 'delete':
                    continue

                if acao == 'mantem':
                    produto_os = form.save(commit=False)
                    produto_os.ordem_servico = ordem_servico
                    produto_os.baixa = baixa_atual  # aqui setamos explicitamente
                    produto_os.save()

                    produto = produto_os.produto
                    quantidade_nova = produto_os.quantidade

                    antigo = next((p for p in produtos_antigos_cop if p.produto.id == produto.id), None)

                    if antigo:
                        baixa_anterior = antigo.baixa
                        quantidade_antiga = antigo.quantidade

                        if baixa_anterior and baixa_atual:
                            # Repor a antiga e subtrair a nova
                            produto.quantidade += quantidade_antiga
                            produto.save()
                            print(f"[REPOSIÇÃO] {produto.nome} -> estoque restaurado: {produto.quantidade}")

                            if produto.quantidade >= quantidade_nova:
                                produto.quantidade -= quantidade_nova
                                produto.save()
                                print(f"[REBAIXA] {produto.nome} -> nova quantidade: {produto.quantidade}")
                            else:
                                messages.error(
                                    request,
                                    f'Estoque insuficiente para o produto \"{produto.nome}\" após reposição. '
                                    f'Estoque atual: {produto.quantidade}, Necessário: {quantidade_nova}'
                                )
                                return render(request, 'ordem_servico/editar_os.html', {
                                    'form': os_form,
                                    'produto_formset': produto_formset,
                                    'ordem_servico': ordem_servico
                                })
                        elif baixa_atual:
                            # Apenas baixa nova
                            produto.quantidade -= quantidade_nova
                            produto.save()
                            print(f"[BAIXA] {produto.nome} -> nova quantidade: {produto.quantidade}")


            messages.success(request, 'Ordem de serviço atualizada com sucesso.')
            return redirect('home')

    else:
        os_form = OrdemServicoForm(instance=ordem_servico)
        produto_formset = ProdutoFormSet(
            queryset=ProdutoOrdemServico.objects.filter(ordem_servico=ordem_servico),
            prefix='form'
        )

    return render(request, 'ordem_servico/editar_os.html', {
        'form': os_form,
        'produto_formset': produto_formset,
        'ordem_servico': ordem_servico
    })



def excluir_os(request, os_id):
    os = get_object_or_404(OrdemServico, id=os_id)
    os.delete()  # Isso também exclui os ProdutoOrdemServico se tiver on_delete=CASCADE
    messages.success(request, 'Ordem de serviço excluída com sucesso.')
    return redirect('home')  # Ou a página que desejar

def ver_os(request, os_id):
    ordem = get_object_or_404(OrdemServico, id=os_id)
    empresa = Empresa.objects.first()
    return render(request, 'ordem_servico/ver_os.html', {'ordem': ordem, "empresa":empresa})

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
    try:
        segmento.delete()
    except ProtectedError:
        mensagem = 'Este segmento está sendo usado por uma Ordem de Serviço e não pode ser excluído.'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})
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
    try:
        unidade.delete()
    except ProtectedError:
        mensagem = 'Este unidade está sendo usado por uma Ordem de Serviço e não pode ser excluído.'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})
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
    try:
        status.delete()
    except ProtectedError:
        mensagem = 'Este status está sendo usado por uma Ordem de Serviço e não pode ser excluído.'
        return render(request, 'principal/erro.html', {'mensagem': mensagem})
    return HttpResponseRedirect(reverse('ordem_servico:definicao') + '?aba=status')