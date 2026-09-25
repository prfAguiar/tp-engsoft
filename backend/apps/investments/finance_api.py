import yfinance as yf

def get_live_asset_data(ticker: str) -> dict:
    """
    Busca dados em tempo real (ou próximo disso) de um ativo usando o yfinance.
    Útil para ações (BOVA11.SA, PETR4.SA) ou FIIs (MXRF11.SA).
    Retorna o preço atual e outras métricas como Dividend Yield.
    """
    if not ticker:
        return {}
        
    try:
        # Instancia o ticker no yfinance
        asset = yf.Ticker(ticker)
        
        # Pega as infos resumidas
        info = asset.info
        
        # Recupera preço atual (pode variar de chave dependendo do ativo)
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
        
        # Recupera Dividend Yield (se aplicável)
        dividend_yield = info.get('dividendYield')
        if dividend_yield is not None:
            # yfinance retorna 0.05 para 5%
            dividend_yield = round(dividend_yield * 100, 2)
            
        return {
            'live_price': current_price,
            'dividend_yield_percent': dividend_yield,
            'currency': info.get('currency', 'BRL'),
            'long_name': info.get('longName'),
            'sector': info.get('sector')
        }
    except Exception as e:
        # Em caso de falha na API ou ticker inválido, retorna vazio para não quebrar a aplicação
        return {'error_fetching_live_data': str(e)}
