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

from .models import Produto, ProdutoOrdemServico, ServicoOrdemServico, DespesaOrdemServico
from .forms import OrdemServicoForm, ProdutoOrdemServicoForm, ServicoOrdemServicoForm
from servicos.models import Servico
from tecnicos.models import Tecnico
from decimal import Decimal  

def criar_despesa(despesa, ordem_servico):
    print("chegou aqui")
    DespesaOrdemServico.objects.create(
        ordem_servico = ordem_servico,
        tipo = despesa['tipo'],
        descricao = despesa['descricao'],
        quantidade = int(despesa['quantidade']),
        preco_unitario = Decimal(despesa['preco_unitario']),
        preco_total = Decimal(despesa['preco_total'])
    )
    print("chegou aqui2")

@login_required
def criar_os(request):
    ProdutoFormSet = modelformset_factory(
        ProdutoOrdemServico,
        form=ProdutoOrdemServicoForm,
        extra=1,
        can_delete=True
    )

    ServicoFormSet = modelformset_factory(
        ServicoOrdemServico,  # Model intermediário que liga serviço à OS
        form=ServicoOrdemServicoForm,
        extra=1,
        can_delete=True
    )

    servicos = Servico.objects.all()
    tecnicos = Tecnico.objects.all()

    if request.method == 'POST':
        os_form = OrdemServicoForm(request.POST, request.FILES)
        produto_formset = ProdutoFormSet(request.POST, prefix='produto')
        servico_formset = ServicoFormSet(request.POST, prefix='servico')

        if os_form.is_valid() and produto_formset.is_valid():
            erro_estoque = False

            # Verifica estoque dos produtos
            for i, form in enumerate(produto_formset.forms):
                acao = request.POST.get(f'produto-{i}-acao', 'mantem')
                if acao == 'mantem':
                    produto = form.cleaned_data.get('produto')
                    quantidade = form.cleaned_data.get('quantidade')

                    if produto and quantidade is not None:
                        try:
                            produto_db = Produto.objects.get(id=produto.id)
                            if produto_db.quantidade < quantidade:
                                erro_estoque = True
                                messages.error(
                                    request,
                                    f"Estoque insuficiente para o produto \"{produto_db.nome}\". "
                                    f"Disponível: {produto_db.quantidade}, Solicitado: {quantidade}"
                                )
                        except Produto.DoesNotExist:
                            erro_estoque = True
                            messages.error(request, 'Produto não encontrado no banco de dados.')

            if erro_estoque:
                return render(request, 'ordem_servico/criar_os.html', {
                    'form': os_form,
                    'produto_formset': produto_formset,
                    'servico_formset': servico_formset,
                    'servicos': servicos,
                    'tecnicos': tecnicos

                })

            # Salva Ordem de Serviço
            ordem_servico = os_form.save(commit=False)
            ordem_servico.digitador = request.user
            ordem_servico.save()

            # Salva os produtos na OS
            for i, form in enumerate(produto_formset.forms):
                acao = request.POST.get(f'produto-{i}-acao', 'mantem')
                if acao == 'delete':
                    continue
                if acao == 'mantem' and form.has_changed():
                    produto_os = form.save(commit=False)
                    produto_os.ordem_servico = ordem_servico
                    produto_os.save()

                    # Baixa estoque
                    produto = Produto.objects.get(id=produto_os.produto.id)
                    produto.quantidade -= produto_os.quantidade
                    produto.save()

            
            # Salva os serviços na OS
            contador = 0

            while True:
                servico_id = request.POST.get(f'form-{contador}-servico')
                tecnico_id = request.POST.get(f'form-{contador}-tecnico')
                quantidade = request.POST.get(f'form-{contador}-quantidade')
                acao = request.POST.get(f'form-{contador}-acao', 'mantem')

                # Se não tem serviço, assume que não há mais blocos
                if servico_id is None:
                    break

                print(f'--- Bloco {contador} ---')
                print('Ação:', acao)

                if acao == 'delete':
                    print('>> Ignorado (delete)')
                    contador += 1
                    continue

                # Tenta buscar os objetos do banco
                servico = tecnico = None
                if tecnico_id and servico_id:
                    servico = Servico.objects.get(id=servico_id)
                    tecnico = Tecnico.objects.get(id=tecnico_id)
                  
                ServicoOrdemServico.objects.create(
                    ordem_servico=ordem_servico,
                    servico=servico,
                    profissional=tecnico,
                    quantidade=quantidade,
                    preco_unitario=servico.preco,
                    preco_total=servico.preco * Decimal(str(quantidade)),
                    comissao= (tecnico.comissao/100)*servico.preco,
                    comissao_total= (tecnico.comissao/100)*(servico.preco * Decimal(str(quantidade))),
                )
                print('Serviço:', servico)
                print('Profissional:', tecnico)
                print('Quantidade:', quantidade)

                contador += 1

            despesas = []
            tipos = [
                'combustivel', 'alimentacao', 'hospedagem', 'mao-de-obra', 'sms', 'consumiveis',
                'comissao', 'locacao', 'outros', 'materia-prima', 'transporte', 'equipamento'
            ]

            for tipo in tipos:
                descricoes = request.POST.getlist(f'descricao_{tipo}')
                quantidades = request.POST.getlist(f'quantidade_{tipo}')
                precos_unitarios = request.POST.getlist(f'preco_unitario_{tipo}')
                precos_totais = request.POST.getlist(f'preco_total_{tipo}')

                for i in range(len(descricoes)):
                    if descricoes[i].strip():  # evita adicionar campos em branco
                        despesas.append({
                            'tipo': tipo,
                            'descricao': descricoes[i],
                            'quantidade': quantidades[i],
                            'preco_unitario': float(precos_unitarios[i]),
                            'preco_total': float(precos_unitarios[i]) * int(quantidades[i])
                        })
            for despesa in despesas:
                print(despesa)
                criar_despesa(despesa, ordem_servico)

            messages.success(request, 'Nova ordem de serviço criada com sucesso.')
            return redirect('ordem_servico:criar_os')

    else:
        os_form = OrdemServicoForm()
        produto_formset = ProdutoFormSet(queryset=ProdutoOrdemServico.objects.none(), prefix='produto')
        servico_formset = ServicoFormSet(queryset=ServicoOrdemServico.objects.none(), prefix='servico')

    nomes = [
    'Combustível', 'Alimentação', 'Hospedagem', 'Mão de obra', 'SMS',
    'Consumíveis', 'Comissão', 'Locação', 'Outros',
    'Matéria Prima', 'Transporte', 'Equipamento'
    ]

    return render(request, 'ordem_servico/criar_os.html', {
        'form': os_form,
        'produto_formset': produto_formset,
        'servico_formset': servico_formset,
        'servicos': servicos,
        'tecnicos': tecnicos,
        'nomes': nomes
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
            produtos_antigos = list(ProdutoOrdemServico.objects.filter(ordem_servico=ordem_servico))
            estoque_temporario = {}

            # Etapa 1 – Repor estoque dos produtos antigos
            for item in produtos_antigos:
                produto = item.produto
                produto.quantidade += item.quantidade
                produto.save()
                estoque_temporario[produto.id] = produto.quantidade

            # Etapa 2 – Validar estoque para novos dados
            for i, form in enumerate(produto_formset.forms):
                if request.POST.get(f'form-{i}-acao', 'mantem') == 'delete':
                    continue

                produto = form.cleaned_data.get('produto')
                quantidade = form.cleaned_data.get('quantidade')

                if produto and quantidade is not None:
                    estoque_atual = estoque_temporario.get(produto.id, produto.quantidade)
                    if estoque_atual < quantidade:
                        erro_estoque = True
                        messages.error(
                            request,
                            f"Estoque insuficiente para o produto '{produto.nome}'. "
                            f"Disponível: {estoque_atual}, Solicitado: {quantidade}"
                        )

            if erro_estoque:
                return render(request, 'ordem_servico/editar_os.html', {
                    'form': os_form,
                    'produto_formset': produto_formset,
                    'ordem_servico': ordem_servico
                })

            # Etapa 3 – Salvar OS e os produtos
            ordem_servico = os_form.save()

            # Remove os antigos do banco
            ProdutoOrdemServico.objects.filter(ordem_servico=ordem_servico).delete()
            
            for i, form in enumerate(produto_formset.forms):
                if request.POST.get(f'form-{i}-acao', 'mantem') == 'delete':
                    continue

                produto_os = form.save(commit=False)
                produto_os.ordem_servico = ordem_servico
                produto_os.save()

                # Recarrega o produto do banco para garantir valor atualizado
                produto = Produto.objects.get(id=produto_os.produto.id)

                print("quantidade a ser tirada (edição):", produto_os.quantidade)
                print("quantidade no estoque (recarregado):", produto.quantidade)

                produto.quantidade -= produto_os.quantidade
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