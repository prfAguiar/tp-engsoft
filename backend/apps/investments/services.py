from decimal import Decimal, ROUND_HALF_UP


def calculate_projection(
    initial_amount: float,
    monthly_contribution: float,
    annual_rate: float,
    period_months: int,
) -> dict:
    """
    Calcula a projeção de rendimento com juros compostos e aportes mensais.

    Fórmula de taxa mensal equivalente: (1 + taxa_anual)^(1/12) - 1
    """
    initial = Decimal(str(initial_amount))
    contribution = Decimal(str(monthly_contribution))
    annual_rate_decimal = Decimal(str(annual_rate)) / Decimal('100')

    # Convertendo taxa anual em taxa mensal de juros compostos
    monthly_rate = Decimal((1 + float(annual_rate_decimal)) ** (1 / 12) - 1)

    current_balance = initial
    total_invested = initial
    evolution = []

    for month in range(1, period_months + 1):
        # Rende sobre o saldo anterior
        interest_month = current_balance * monthly_rate
        current_balance += interest_month + contribution
        total_invested += contribution

        total_interest = current_balance - total_invested

        evolution.append({
            'month': month,
            'invested_amount': float(
                total_invested.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            ),
            'interest_earned': float(
                total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            ),
            'total_balance': float(
                current_balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            ),
        })

    total_interest_final = current_balance - total_invested

    return {
        'initial_amount': float(initial.quantize(Decimal('0.01'))),
        'total_contributions': float(
            (total_invested - initial).quantize(Decimal('0.01'))
        ),
        'total_invested': float(
            total_invested.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        ),
        'total_interest_earned': float(
            total_interest_final.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        ),
        'final_balance': float(
            current_balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        ),
        'period_months': period_months,
        'annual_rate_percent': annual_rate,
        'evolution': evolution,
    }


def generate_investment_suggestion(
    amount: float,
    investor_profile: str,
    wallet=None,
) -> dict:
    """
    Gera uma sugestão de alocação de investimentos baseada no montante,
    no perfil de investidor e, se disponível, na carteira atual do usuário
    (rebalanceamento inteligente direcionando os novos aportes).
    """
    from .strategies import ALLOCATION_PROFILES
    from .models import Investment

    profile_info = ALLOCATION_PROFILES.get(investor_profile)
    if not profile_info:
        raise ValueError(f"Perfil de investidor '{investor_profile}' não reconhecido.")

    contribution_amount = Decimal(str(amount))
    allocations_config = profile_info['allocations']

    # 1. Mapeia patrimônio atual da carteira por tipo de ativo (se fornecida)
    current_by_type = {item['type']: Decimal('0.00') for item in allocations_config}
    has_wallet_items = False

    if wallet:
        for item in wallet.items.select_related('investment').all():
            has_wallet_items = True
            inv_type = item.investment.type
            if inv_type in current_by_type:
                current_by_type[inv_type] += Decimal(str(item.amount))
            else:
                current_by_type[inv_type] = Decimal(str(item.amount))

    total_current_portfolio = sum(current_by_type.values())
    projected_total = total_current_portfolio + contribution_amount

    # 2. Calcula déficit ou peso para cada classe
    target_weights = {item['type']: Decimal(str(item['percentage'])) / Decimal('100') for item in allocations_config}

    from .rebalance import calculate_rebalanced_allocation

    if has_wallet_items and total_current_portfolio > Decimal('0.00'):
        allocated_breakdown = calculate_rebalanced_allocation(
            projected_total=projected_total,
            contribution_amount=contribution_amount,
            target_weights=target_weights,
            current_by_type=current_by_type,
        )
    else:
        # Alocação pura pelo perfil (iniciante ou carteira zerada)
        accumulated = Decimal('0.00')
        type_keys = list(target_weights.keys())
        allocated_breakdown = {}
        for idx, inv_type in enumerate(type_keys):
            if idx == len(type_keys) - 1:
                allocated_breakdown[inv_type] = contribution_amount - accumulated
            else:
                val = (contribution_amount * target_weights[inv_type]).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )
                allocated_breakdown[inv_type] = val
                accumulated += val

    # 3. Busca ativos reais cadastrados no banco para enriquecer a recomendação
    catalog_assets_by_type = {}
    for inv in Investment.objects.all():
        catalog_assets_by_type.setdefault(inv.type, []).append(
            f"{inv.name} ({inv.ticker})" if inv.ticker else inv.name
        )

    # 4. Monta resultado
    result_allocations = []
    for item in allocations_config:
        inv_type = item['type']
        allocated_val = allocated_breakdown.get(inv_type, Decimal('0.00'))
        allocated_pct = (
            float((allocated_val / contribution_amount * Decimal('100')).quantize(Decimal('0.1')))
            if contribution_amount > Decimal('0.00') else 0.0
        )

        catalog_assets = catalog_assets_by_type.get(inv_type, [])
        suggested = catalog_assets if catalog_assets else item['suggested_assets']

        result_allocations.append({
            'type': inv_type,
            'category': item['category'],
            'target_percentage': float(item['percentage']),
            'allocation_percentage': allocated_pct,
            'allocated_amount': float(allocated_val.quantize(Decimal('0.01'))),
            'current_holdings': float(current_by_type.get(inv_type, Decimal('0.00'))),
            'suggested_assets': suggested,
            'description': item['description'],
        })

    return {
        'total_amount': float(contribution_amount.quantize(Decimal('0.01'))),
        'investor_profile': profile_info['profile_name'],
        'profile_label': profile_info['profile_label'],
        'rebalanced': has_wallet_items and total_current_portfolio > Decimal('0.00'),
        'current_portfolio_total': float(total_current_portfolio.quantize(Decimal('0.01'))),
        'allocations': result_allocations,
    }
