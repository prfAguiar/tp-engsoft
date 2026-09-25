from rest_framework import serializers


class ProjectionInputSerializer(serializers.Serializer):
    initial_amount = serializers.FloatField(
        min_value=0.0,
        default=0.0,
        help_text="Montante inicial a ser investido",
    )
    monthly_contribution = serializers.FloatField(
        min_value=0.0,
        default=0.0,
        help_text="Valor do aporte mensal",
    )
    annual_rate = serializers.FloatField(
        min_value=0.0,
        max_value=100.0,
        help_text="Taxa de juros anual estimada em porcentagem (ex: 10.5 para 10.5%)",
    )
    period_months = serializers.IntegerField(
        min_value=1,
        max_value=600,
        help_text="Período do investimento em meses (ex: 12 a 600 meses)",
    )


class InvestmentSuggestionInputSerializer(serializers.Serializer):
    amount = serializers.FloatField(
        min_value=1.0,
        help_text="Montante total a ser alocado em investimentos (em R$)",
    )
    investor_profile = serializers.ChoiceField(
        choices=['CONSERVATIVE', 'MODERATE', 'AGGRESSIVE'],
        required=False,
        allow_null=True,
        help_text="Perfil de investidor desejado (caso omitido, usa o do usuário autenticado)",
    )
