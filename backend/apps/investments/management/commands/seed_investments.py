from django.core.management.base import BaseCommand
from apps.investments.models import Investment

class Command(BaseCommand):
    help = 'Povoa o banco de dados com ativos reais (Ações, FIIs e Renda Fixa) para consumo da corretora.'

    def handle(self, *args, **kwargs):
        assets = [
            {
                'name': 'Itaú Unibanco',
                'ticker': 'ITUB4.SA',
                'type': 'STOCK',
                'risk_level': 'HIGH',
                'liquidity_deadline': 2,
                'description': 'Ação do maior banco privado da América Latina, forte pagadora de dividendos.'
            },
            {
                'name': 'Petrobras',
                'ticker': 'PETR4.SA',
                'type': 'STOCK',
                'risk_level': 'HIGH',
                'liquidity_deadline': 2,
                'description': 'Empresa estatal de petróleo com distribuição massiva de proventos.'
            },
            {
                'name': 'Maxi Renda FII',
                'ticker': 'MXRF11.SA',
                'type': 'FII',
                'risk_level': 'MEDIUM',
                'liquidity_deadline': 2,
                'description': 'Fundo imobiliário de papel mais popular do Brasil (base 10).'
            },
            {
                'name': 'Tesouro Selic 2029',
                'ticker': '',
                'type': 'FIXED_INCOME',
                'risk_level': 'LOW',
                'profitability': 10.50,
                'liquidity_deadline': 1,
                'description': 'Título público mais seguro do mercado, ideal para reserva de emergência.'
            },
            {
                'name': 'CDB Banco Master',
                'ticker': '',
                'type': 'FIXED_INCOME',
                'risk_level': 'LOW',
                'profitability': 12.00,
                'liquidity_deadline': 365,
                'description': 'CDB com ótima rentabilidade fixada para vencimento no médio prazo.'
            }
        ]

        created_count = 0
        for asset_data in assets:
            obj, created = Investment.objects.get_or_create(
                name=asset_data['name'],
                defaults=asset_data
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Sucesso! {created_count} novos ativos inseridos no catálogo de investimentos da corretora.'))
