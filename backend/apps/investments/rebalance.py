from decimal import Decimal, ROUND_HALF_UP


def calculate_rebalanced_allocation(
    projected_total: Decimal,
    contribution_amount: Decimal,
    target_weights: dict[str, Decimal],
    current_by_type: dict[str, Decimal],
) -> dict[str, Decimal]:
    """
    Calcula a distribuição de um novo aporte financeiro com base no déficit
    de cada categoria em relação à alocação ideal da carteira.
    """
    deficits = {}
    for inv_type, weight in target_weights.items():
        target_amount = projected_total * weight
        current_amt = current_by_type.get(inv_type, Decimal('0.00'))
        deficit = max(Decimal('0.00'), target_amount - current_amt)
        deficits[inv_type] = deficit

    total_deficit = sum(deficits.values())
    allocated_breakdown = {}

    if total_deficit > Decimal('0.00'):
        accumulated = Decimal('0.00')
        type_keys = list(target_weights.keys())
        for idx, inv_type in enumerate(type_keys):
            if idx == len(type_keys) - 1:
                allocated_breakdown[inv_type] = contribution_amount - accumulated
            else:
                share = (deficits[inv_type] / total_deficit) * contribution_amount
                val = share.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                allocated_breakdown[inv_type] = val
                accumulated += val
    else:
        # Sem déficit: distribui conforme os pesos padrão do perfil
        accumulated = Decimal('0.00')
        type_keys = list(target_weights.keys())
        for idx, inv_type in enumerate(type_keys):
            if idx == len(type_keys) - 1:
                allocated_breakdown[inv_type] = contribution_amount - accumulated
            else:
                val = (contribution_amount * target_weights[inv_type]).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )
                allocated_breakdown[inv_type] = val
                accumulated += val

    return allocated_breakdown
