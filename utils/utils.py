
def formata_preco(val):
    try:
        val = float(val)  # Tenta converter para float
    except ValueError:
        return val  # Se falhar, retorna o valor original (pode ser uma string inválida)
    return f'R$ {val:.2f}'.replace('.', ',')

def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])

def cart_totals(carrinho):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for item in carrinho.values()
        ]
    )
