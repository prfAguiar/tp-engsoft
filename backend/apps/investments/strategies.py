"""
Estratégias e matriz de alocação de investimentos por perfil de risco.
"""

ALLOCATION_PROFILES = {
    'CONSERVATIVE': {
        'profile_name': 'CONSERVATIVE',
        'profile_label': 'Conservador',
        'allocations': [
            {
                'category': 'Renda Fixa Pós-Fixada',
                'percentage': 70.0,
                'suggested_assets': ['Tesouro Selic', 'CDB 100%+ CDI com liquidez diária'],
                'description': 'Alta liquidez e segurança para preservação de capital.',
            },
            {
                'category': 'Renda Fixa Inflação',
                'percentage': 20.0,
                'suggested_assets': ['Tesouro IPCA+', 'LCI/LCA indexada ao IPCA'],
                'description': 'Proteção do poder de compra contra a inflação no médio prazo.',
            },
            {
                'category': 'Fundos Imobiliários',
                'percentage': 10.0,
                'suggested_assets': ['FIIs de papel high grade (KNSC11, KNCR11)'],
                'description': 'Geração de renda passiva com menor volatilidade relativa.',
            },
        ],
    },
    'MODERATE': {
        'profile_name': 'MODERATE',
        'profile_label': 'Moderado',
        'allocations': [
            {
                'category': 'Renda Fixa Pós-Fixada e Inflação',
                'percentage': 40.0,
                'suggested_assets': ['Tesouro Selic', 'Tesouro IPCA+'],
                'description': 'Base sólida de segurança e preservação de capital.',
            },
            {
                'category': 'Fundos Imobiliários',
                'percentage': 30.0,
                'suggested_assets': ['FIIs híbridos, tijolo e papel (HGLG11, MXRF11)'],
                'description': 'Renda passiva recorrente com potencial de valorização.',
            },
            {
                'category': 'Ações Nacionais',
                'percentage': 25.0,
                'suggested_assets': ['ETFs (BOVA11, SMAL11) e Ações de valor/dividendos (ITUB4, VALE3)'],
                'description': 'Participação em empresas consolidadas para valorização de médio/longo prazo.',
            },
            {
                'category': 'Internacional / Alternativos',
                'percentage': 5.0,
                'suggested_assets': ['ETFs globais (IVVB11, ACWI11)'],
                'description': 'Diversificação cambial e exposição à economia global.',
            },
        ],
    },
    'AGGRESSIVE': {
        'profile_name': 'AGGRESSIVE',
        'profile_label': 'Agressivo',
        'allocations': [
            {
                'category': 'Renda Fixa',
                'percentage': 20.0,
                'suggested_assets': ['Tesouro Selic com liquidez imediata'],
                'description': 'Reserva de liquidez para aportes de oportunidade.',
            },
            {
                'category': 'Ações Nacionais',
                'percentage': 35.0,
                'suggested_assets': ['Ações de crescimento e dividendos (WEGE3, PRIO3, BBAS3)'],
                'description': 'Foco em valorização patrimonial acelerada e retornos robustos.',
            },
            {
                'category': 'Fundos Imobiliários',
                'percentage': 25.0,
                'suggested_assets': ['FIIs de Tijolo e desenvolvimento imobiliário'],
                'description': 'Fluxo contínuo de proventos com reinvestimento estratégico.',
            },
            {
                'category': 'Internacional / Alternativos',
                'percentage': 20.0,
                'suggested_assets': ['ETFs globais (IVVB11, SPXI11) e Criptoativos (Bitcoin/Ethereum)'],
                'description': 'Máxima diversificação geográfica e busca de alfa.',
            },
        ],
    },
}
