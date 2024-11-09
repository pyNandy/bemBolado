class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista_doces')
            )
        alteracao_id = self.request.GET.get("vid")

        if not alteracao_id:
            messages.error(
                self.request,
                'Prduto nao existe'
            )
            return redirect(http_referer)
        
        alteracao = get_object_or_404(models.Alteracao, id=alteracao_id )
        alteracao_estoque = alteracao.estoque_3
        produto = alteracao.produto

        produto_id = produto.id
        produto_nome = produto.nome_produto_3
        alteracao_nome = alteracao.nome_variacao or ''
        preco_unitario = alteracao.preco_venda
        preco_unitario_promocional = alteracao.preco_venda_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if alteracao.estoque_3 < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'    
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
        
        carrinho = self.request.session['carrinho']

        if alteracao_id in carrinho:
            quantidade_carrinho = carrinho[alteracao_id]['quantidade']
            quantidade_carrinho += 1

            if alteracao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insulficiente para {quantidade_carrinho} x no'
                    f'produto"{produto_nome}". Adicionamos {alteracao_estoque} x'
                    f"no seu carrinho ."
                )
                quantidade_carrinho = alteracao_estoque
            
            print(quantidade_carrinho)

                
            carrinho[alteracao_id]["quantidade"] = quantidade_carrinho

            carrinho[alteracao_id]["preco_quantitativo"] = preco_unitario * \
                quantidade_carrinho
            
            carrinho[alteracao_id]["preco_quantitativo_promocional"] = preco_unitario_promocional * \
                quantidade_carrinho

        else:
            carrinho[alteracao_id] = {                            
                "produto_id" : produto_id,
                "produto_nome":produto_nome,
                "alteracao_nome" : alteracao_nome,
                "alteracao_id" : alteracao_id,
                "preco_unitario" :preco_unitario,
                "preco_unitario_promocional":preco_unitario_promocional,
                "preco_quantitativo":preco_unitario,
                "preco_quantitativo_promocional": preco_unitario_promocional,
                "quantidade": 1,
                "slug": slug,
                "imagem": imagem,
            }
            
        self.request.session.save()

        messages.success(
            self.request,
            f'Produto: {produto_nome}, tamanho: {alteracao_nome} foi adicionado ao seu carrinho'
            f'carrinho {carrinho[alteracao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)