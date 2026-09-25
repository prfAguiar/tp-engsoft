import yfinance as yf
from django.core.cache import cache

# Tempo em segundos que os dados de um ticker ficam em cache (5 minutos)
LIVE_DATA_CACHE_TTL = 300


def get_live_asset_data(ticker: str) -> dict:
    """
    Busca dados em tempo real (ou próximo disso) de um ativo usando o yfinance.
    Útil para ações (BOVA11.SA, PETR4.SA) ou FIIs (MXRF11.SA).
    Retorna o preço atual e outras métricas como Dividend Yield.

    Os dados são mantidos em cache por LIVE_DATA_CACHE_TTL segundos para evitar
    chamadas repetidas à API externa a cada requisição do catálogo.
    """
    if not ticker:
        return {}

    cache_key = f'live_asset_data_{ticker}'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    try:
        # Instancia o ticker no yfinance
        asset = yf.Ticker(ticker)

        # Pega as infos resumidas
        info = asset.info

        # Recupera preço atual (pode variar de chave dependendo do ativo)
        current_price = (
            info.get('currentPrice')
            or info.get('regularMarketPrice')
            or info.get('previousClose')
        )

        # Recupera Dividend Yield (se aplicável)
        dividend_yield = info.get('dividendYield')
        if dividend_yield is not None:
            # yfinance retorna 0.05 para 5%
            dividend_yield = round(dividend_yield * 100, 2)

        result = {
            'live_price': current_price,
            'dividend_yield_percent': dividend_yield,
            'currency': info.get('currency', 'BRL'),
            'long_name': info.get('longName'),
            'sector': info.get('sector'),
        }

        cache.set(cache_key, result, LIVE_DATA_CACHE_TTL)
        return result

    except Exception:
        # Em caso de falha na API externa ou ticker inválido, retorna vazio
        # sem vazar detalhes internos do erro para o consumidor da API.
        return {}
