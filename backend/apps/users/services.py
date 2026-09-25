"""
Serviço para cálculo e avaliação de perfil de investidor (suitability).
"""

PROFILES = {
    'CONSERVATIVE': {
        'name': 'CONSERVATIVE',
        'label': 'Conservador',
        'description': (
            'Prioriza a preservação de capital com risco mínimo. '
            'Tem baixa tolerância à volatilidade e busca liquidez e segurança.'
        ),
    },
    'MODERATE': {
        'name': 'MODERATE',
        'label': 'Moderado',
        'description': (
            'Busca equilíbrio entre segurança e rentabilidade. '
            'Tolera pequenas oscilações de curto prazo visando retornos maiores no médio/longo prazo.'
        ),
    },
    'AGGRESSIVE': {
        'name': 'AGGRESSIVE',
        'label': 'Agressivo',
        'description': (
            'Foca em maximizar a rentabilidade no longo prazo. '
            'Aceita riscos e alta volatilidade em troca do potencial de ganhos superiores.'
        ),
    },
}

QUIZ_QUESTIONS = [
    {
        'id': 'horizon',
        'question': 'Por quanto tempo você pretende manter o seu dinheiro investido?',
        'options': [
            {'value': 1, 'text': 'Menos de 1 ano'},
            {'value': 2, 'text': 'Entre 1 e 5 anos'},
            {'value': 3, 'text': 'Mais de 5 anos'},
        ],
    },
    {
        'id': 'reaction',
        'question': 'Como você reage ao ver seus investimentos oscilando negativamente no curto prazo?',
        'options': [
            {'value': 1, 'text': 'Fico desconfortável e resgataria imediatamente'},
            {'value': 2, 'text': 'Entendo a volatilidade e aguardo a recuperação'},
            {'value': 3, 'text': 'Enxergo como oportunidade e aporto mais recursos'},
        ],
    },
    {
        'id': 'knowledge',
        'question': 'Qual é o seu nível de conhecimento sobre o mercado financeiro e investimentos?',
        'options': [
            {'value': 1, 'text': 'Iniciante, conheço apenas poupança e renda fixa simples'},
            {'value': 2, 'text': 'Intermediário, conheço fundos, CDBs, Tesouro Direto e um pouco de ações'},
            {'value': 3, 'text': 'Avançado, opero ou compreendo ações, FIIs, derivativos e renda variável'},
        ],
    },
    {
        'id': 'goal',
        'question': 'Qual é o seu objetivo financeiro prioritário?',
        'options': [
            {'value': 1, 'text': 'Preservar meu patrimônio sem correr riscos de perda'},
            {'value': 2, 'text': 'Superar a inflação com crescimento moderado do capital'},
            {'value': 3, 'text': 'Multiplicar meu patrimônio buscando a maior rentabilidade possível'},
        ],
    },
]


def calculate_investor_profile(scores: list[int]) -> dict:
    """
    Calcula o perfil de investidor a partir das pontuações das respostas.
    - Até 6 pontos: Conservador
    - 7 a 9 pontos: Moderado
    - 10 a 12 pontos: Agressivo
    """
    total_score = sum(scores)

    if total_score <= 6:
        profile_key = 'CONSERVATIVE'
    elif total_score <= 9:
        profile_key = 'MODERATE'
    else:
        profile_key = 'AGGRESSIVE'

    profile_data = PROFILES[profile_key]
    return {
        'profile': profile_data['name'],
        'profile_label': profile_data['label'],
        'description': profile_data['description'],
        'total_score': total_score,
        'min_score': len(scores) * 1,
        'max_score': len(scores) * 3,
    }
