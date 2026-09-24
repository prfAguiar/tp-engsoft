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
