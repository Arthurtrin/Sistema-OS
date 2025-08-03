from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrdemServico, Status, Unidade, Segmento, ProdutoOrdemServico, ServicoOrdemServico, DespesaOrdemServico
from .forms import SegmentoForm, StatusForm, UnidadeForm, OrdemServicoForm, ProdutoOrdemServicoForm
from produtos.models import Produto
from usuarios.models import Perfil, Chave_Gerenciador
from configuracoes.models import Empresa
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
from django.contrib import messages
from django.db.models import ProtectedError
from servicos.models import Servico
from tecnicos.models import Tecnico
from decimal import Decimal  
from django.db.models import Sum

# Salva os despesas na OS
def criar_despesa(request, ordem_servico):
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
        DespesaOrdemServico.objects.create(
            ordem_servico = ordem_servico,
            tipo = despesa['tipo'],
            descricao = despesa['descricao'],
            quantidade = int(despesa['quantidade']),
            preco_unitario = Decimal(despesa['preco_unitario']),
            preco_total = Decimal(despesa['preco_total'])
        )

# Salva os serviços na OS
def criar_servico(request, ordem_servico):
    total_forms = int(request.POST.get('servico-TOTAL_FORMS', 0))

    for i in range(total_forms):
        servico_id = request.POST.get(f'form-{i}-servico')
        tecnico_id = request.POST.get(f'form-{i}-tecnico')
        quantidade_lista = request.POST.getlist(f'form-{i}-quantidade-servico')
        quantidade = quantidade_lista[0] if quantidade_lista else None
        acao = request.POST.get(f'form-{i}-acao', 'mantem')

        if not servico_id or acao != 'mantem':
            continue

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

def verifica_produto_estoque(request, produto_id, quantidade, erro_estoque):
    try:
        produto = Produto.objects.get(id=produto_id)
        if produto.quantidade < int(quantidade):
            erro_estoque = True
            messages.error(
                request,
                f"Estoque insuficiente para o produto \"{produto.nome}\". "
                f"Disponível: {produto.quantidade}, Solicitado: {quantidade}"
                )
    except Produto.DoesNotExist:
        erro_estoque = True
        messages.error(request, 'Produto não encontrado no banco de dados.')
    return erro_estoque

@login_required
def criar_os(request):
    servicos = Servico.objects.all()
    tecnicos = Tecnico.objects.all()
    produtos = Produto.objects.all()
    nomes = [
        'Combustível', 'Alimentação', 'Hospedagem', 'Mão de obra', 'SMS',
        'Consumíveis', 'Comissão', 'Locação', 'Outros',
        'Matéria Prima', 'Transporte', 'Equipamento'
    ]

    if request.method == 'POST':
        os_form = OrdemServicoForm(request.POST, request.FILES)
        
        if os_form.is_valid():
            erro_estoque = False
            total_forms = int(request.POST.get('form-TOTAL_FORMS', 0))
            for i in range(total_forms):
                produto_id = request.POST.get(f'form-{i}-produto')
                quantidade_lista = request.POST.getlist(f'form-{i}-quantidade')
                quantidade = quantidade_lista[0] if quantidade_lista else None
                acao = request.POST.get(f'form-{i}-acao', 'mantem')

                if not produto_id or acao != 'mantem':
                    continue
                
                erro_estoque = verifica_produto_estoque(request, produto_id, quantidade, erro_estoque)
                
            if erro_estoque:
                return render(request, 'ordem_servico/criar_os.html', {
                    'form': os_form,
                    'servicos': servicos,
                    'tecnicos': tecnicos,
                    'nomes': nomes,
                    'produtos': produtos
                })

            # Salva Ordem de Serviço
            ordem_servico = os_form.save(commit=False)
            ordem_servico.digitador = request.user
            ordem_servico.save()

            # Salva os produtos na OS
            for i in range(total_forms):
                produto_id = request.POST.get(f'form-{i}-produto')
                quantidade_lista = request.POST.getlist(f'form-{i}-quantidade')
                quantidade = quantidade_lista[0] if quantidade_lista else None
                acao = request.POST.get(f'produto-{i}-acao', 'mantem')

                if not produto_id or acao != 'mantem':
                    continue

                produto = Produto.objects.get(id=produto_id)
                ProdutoOrdemServico.objects.create(
                    ordem_servico = ordem_servico,
                    produto = produto,
                    quantidade = quantidade
                )

                # Baixa estoque
                produto = Produto.objects.get(id=produto_id)
                produto.quantidade -= int(quantidade)
                produto.save()

            criar_servico(request, ordem_servico)
            criar_despesa(request, ordem_servico)

            messages.success(request, 'Nova ordem de serviço criada com sucesso.')
            return redirect('ordem_servico:criar_os')
    else:

        os_form = OrdemServicoForm()
    return render(request, 'ordem_servico/criar_os.html', {
        'form': os_form,
        'servicos': servicos,
        'tecnicos': tecnicos,
        'nomes': nomes,
        'produtos': produtos
    })


@login_required
def editar_os(request, os_id):
    ordem_servico = get_object_or_404(OrdemServico, id=os_id)
    somatoria_produtos = ordem_servico.itens.all()
    somatoria_servicos = ordem_servico.servicos.all()
    somatoria_despesas = ordem_servico.despesas.all()
    
    servicos = Servico.objects.all()
    tecnicos = Tecnico.objects.all()
    produtos = Produto.objects.all()

    nomes = [
        'Combustível', 'Alimentação', 'Hospedagem', 'Mão de obra', 'SMS',
        'Consumíveis', 'Comissão', 'Locação', 'Outros',
        'Matéria Prima', 'Transporte', 'Equipamento'
    ]

    if request.method == 'POST':
        os_form = OrdemServicoForm(request.POST, request.FILES, instance=ordem_servico)

        if os_form.is_valid():
            erro_estoque = False
            despesas = ordem_servico.despesas.all()
            novas_despesas = []

            for i, despesa in enumerate(ordem_servico.despesas.all()):
                tipo = request.POST.get(f"despesa-{i}-tipo")
                descricao = request.POST.get(f"descricao_{despesa.id}")
                quantidade = request.POST.get(f"quantidade_{despesa.id}")
                preco_unitario = request.POST.get(f"preco_unitario_{despesa.id}")
                preco_total = request.POST.get(f"preco_total_{despesa.id}")

                if all(x is None for x in [tipo, descricao, quantidade, preco_unitario, preco_total]):
                    continue
                
                novas_despesas.append({
                    'tipo': tipo,
                    'descricao': descricao,
                    'quantidade': quantidade,
                    'preco_unitario': preco_unitario,
                    'preco_total': preco_total,
                })

            # Exclui as despesas antigas
            ordem_servico.despesas.all().delete()

            # Cria novas despesas
            for item in novas_despesas:
                DespesaOrdemServico.objects.create(
                    ordem_servico=ordem_servico,
                    tipo=item['tipo'],
                    descricao=item['descricao'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco_unitario'],
                    preco_total=item['preco_total'],
                )
            criar_despesa(request, ordem_servico)

            servicos_cad = []
            for i, _ in enumerate(ordem_servico.servicos.all()):
                servico_id = request.POST.get(f'servico_{i}')
                tecnico_id = request.POST.get(f'tecnico_{i}')
                quantidade_serv = request.POST.get(f'quantidade_{i}')
                preco_unitario_serv = request.POST.get(f'preco_unitario_{i}')
                preco_total_serv = request.POST.get(f'preco_total_{i}')
                comissao = request.POST.get(f'comissao_{i}')
                comissao_total = request.POST.get(f'comissao_total_{i}')

                if all(x is None for x in [servico_id, tecnico_id, quantidade_serv, preco_unitario_serv, preco_total_serv, comissao, comissao_total]):
                    continue
                servico = Servico.objects.get(id=servico_id)
                tecnico = Tecnico.objects.get(id=tecnico_id)

                servicos_cad.append({
                'servico': servico,
                'tecnico': tecnico,
                'quantidade': quantidade_serv,
                'preco_unitario': preco_unitario_serv,
                'preco_total': preco_total_serv,
                'comissao': comissao,
                'comissao_total': comissao_total,
            })
            
            ordem_servico.servicos.all().delete() 
            for item in servicos_cad:
                ServicoOrdemServico.objects.create(
                    ordem_servico=ordem_servico,  # certifique-se de que essa variável está definida
                    servico=item['servico'],
                    profissional=item['tecnico'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco_unitario'],
                    preco_total=item['preco_total'],
                    comissao=item['comissao'],
                    comissao_total=item['comissao_total'],
                )
            criar_servico(request, ordem_servico)
            
            for item in ordem_servico.itens.all():
                produto = item.produto  
                produto.quantidade += item.quantidade  # Devolve ao estoque
                produto.save()

            produtos_cad = []
            for i, _ in enumerate(ordem_servico.itens.all()):
                produto_nome = request.POST.get(f'produto_{i}')
                quantidade_produto = request.POST.get(f'quantidade_{i}')
                print(produto_nome, quantidade_produto)

                if all(x is None for x in [produto_nome, quantidade_produto]):
                    continue
                
                produtos_cad.append({
                    'produto_nome': produto_nome,
                    'quantidade': quantidade_produto
                })

            #for item in ordem_servico.itens.all():
            #    produto = item.produto
            #    print(produto.nome)
    else:
        os_form = OrdemServicoForm(instance=ordem_servico)
        

        return render(request, 'ordem_servico/editar_os.html', {
            'form': os_form,
            'ordem_servico': ordem_servico,
            'somatoria_produtos': somatoria_produtos,
            'somatoria_servicos': somatoria_servicos,
            'somatoria_despesas': somatoria_despesas,
            'produtos': produtos,
            'servicos': servicos,
            'tecnicos': tecnicos,
            'nomes': nomes,
            'tipos_despesa': DespesaOrdemServico.TIPO_CHOICES,
        })

"""
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

"""

def excluir_os(request, os_id):
    os = get_object_or_404(OrdemServico, id=os_id)
    os.delete()  # Isso também exclui os ProdutoOrdemServico se tiver on_delete=CASCADE
    messages.success(request, 'Ordem de serviço excluída com sucesso.')
    return redirect('home')  # Ou a página que desejar

def ver_os(request, os_id):
    ordem = get_object_or_404(OrdemServico, id=os_id)
    empresa = Empresa.objects.first()
    gasto_total_despesa = ordem.despesas.aggregate(total=Sum('preco_total'))['total'] or 0

    gasto_comissao_servico = ordem.servicos.aggregate(total=Sum('comissao_total'))['total'] or 0
    gasto_preco_servico = ordem.servicos.aggregate(total=Sum('preco_total'))['total'] or 0
    gasto_total_servico = gasto_comissao_servico + gasto_preco_servico

    gasto_total = gasto_total_servico + gasto_total_despesa

    return render(request, 'ordem_servico/ver_os.html', {
        'ordem': ordem, 
        "empresa":empresa,
        "gasto_despesa":float(gasto_total_despesa),
        "gasto_servico":float(gasto_total_servico),
        "gasto_total":float(gasto_total)})

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