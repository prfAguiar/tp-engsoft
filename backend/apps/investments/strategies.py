"""
Estratégias e matriz de alocação de investimentos por perfil de risco.
"""

ALLOCATION_PROFILES = {
    'CONSERVATIVE': {
        'profile_name': 'CONSERVATIVE',
        'profile_label': 'Conservador',
        'allocations': [
            {
                'type': 'FIXED_INCOME',
                'category': 'Renda Fixa',
                'percentage': 85.0,
                'suggested_assets': ['Tesouro Selic 2029', 'CDB Banco Master'],
                'description': 'Alta liquidez e segurança para preservação de capital e reserva.',
            },
            {
                'type': 'FII',
                'category': 'Fundos Imobiliários',
                'percentage': 10.0,
                'suggested_assets': ['Maxi Renda FII (MXRF11.SA)'],
                'description': 'Geração de renda passiva com menor volatilidade relativa.',
            },
            {
                'type': 'STOCK',
                'category': 'Ações Nacionais',
                'percentage': 5.0,
                'suggested_assets': ['Itaú Unibanco (ITUB4.SA)'],
                'description': 'Pequena exposição em empresas líderes com foco em dividendos.',
            },
        ],
    },
    'MODERATE': {
        'profile_name': 'MODERATE',
        'profile_label': 'Moderado',
        'allocations': [
            {
                'type': 'FIXED_INCOME',
                'category': 'Renda Fixa',
                'percentage': 45.0,
                'suggested_assets': ['Tesouro Selic 2029', 'CDB Banco Master'],
                'description': 'Base sólida de segurança e preservação de capital.',
            },
            {
                'type': 'FII',
                'category': 'Fundos Imobiliários',
                'percentage': 30.0,
                'suggested_assets': ['Maxi Renda FII (MXRF11.SA)'],
                'description': 'Renda passiva recorrente com potencial de valorização.',
            },
            {
                'type': 'STOCK',
                'category': 'Ações Nacionais',
                'percentage': 25.0,
                'suggested_assets': ['Itaú Unibanco (ITUB4.SA)', 'Petrobras (PETR4.SA)'],
                'description': 'Participação em empresas consolidadas para valorização no longo prazo.',
            },
        ],
    },
    'AGGRESSIVE': {
        'profile_name': 'AGGRESSIVE',
        'profile_label': 'Agressivo',
        'allocations': [
            {
                'type': 'STOCK',
                'category': 'Ações Nacionais',
                'percentage': 50.0,
                'suggested_assets': ['Petrobras (PETR4.SA)', 'Itaú Unibanco (ITUB4.SA)'],
                'description': 'Foco em valorização patrimonial acelerada e retornos robustos.',
            },
            {
                'type': 'FII',
                'category': 'Fundos Imobiliários',
                'percentage': 30.0,
                'suggested_assets': ['Maxi Renda FII (MXRF11.SA)'],
                'description': 'Fluxo contínuo de proventos com reinvestimento estratégico.',
            },
            {
                'type': 'FIXED_INCOME',
                'category': 'Renda Fixa',
                'percentage': 20.0,
                'suggested_assets': ['Tesouro Selic 2029'],
                'description': 'Reserva de liquidez para aportes de oportunidade.',
            },
        ],
    },
}
