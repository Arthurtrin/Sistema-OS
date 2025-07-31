def criar_servico(request, ordem_servico):
    total_forms = int(request.POST.get('servico-TOTAL_FORMS', 0))
        try:
            for i in range(total_forms):
                servico_id = request.POST.get(f'form-{i}-servico')
                tecnico_id = request.POST.get(f'form-{i}-tecnico')
                quantidade_lista = request.POST.getlist(f'form-{i}-quantidade')
                quantidade = quantidade_lista[0] if quantidade_lista else None
                acao = request.POST.get(f'form-{i}-acao', 'mantem')

                if not produto_id or acao != 'mantem':
                    continue
                
                servico = Servico.objects.get(id=servico_id)
                tecnico = Tecnico.objects.get(id=tecnico_id)
                print(servico)
                print(tecnico)
                print(quantidade)
                print(acao)
                
"""
                # Se não tem serviço, assume que não há mais blocos
                if not produto_id or acao != 'mantem':
                    continue

                try:
                    servico = Servico.objects.get(id=servico_id)
                    tecnico = Tecnico.objects.get(id=tecnico_id)
                except:
                    messages.error(
                            request,
                            f"Não foi encontrado"
                            f"Disponível: {produto.quantidade}, Solicitado: {quantidade}"
                        )
                #cria uma instancia de ServicoOrdemServico
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
                contador += 1    
        except:
            print("deu erro na parte de serviço, mané")"""
            