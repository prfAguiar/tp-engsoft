import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.investments.models import Investment

def seed():
    # Clear existing to avoid duplicates if run multiple times
    Investment.objects.all().delete()
    
    # Renda Fixa (Sem Ticker)
    Investment.objects.create(
        name="Tesouro Selic 2029",
        type="FIXED_INCOME",
        risk_level="LOW",
        profitability=10.50,
        liquidity_deadline=0,
        description="Título público federal com rentabilidade atrelada à Selic."
    )
    
    Investment.objects.create(
        name="CDB Banco Master",
        type="FIXED_INCOME",
        risk_level="MEDIUM",
        profitability=12.50,
        liquidity_deadline=365,
        description="CDB com rentabilidade prefixada."
    )
    
    # Ações (Com Ticker)
    Investment.objects.create(
        name="Itaú Unibanco",
        ticker="ITUB4.SA",
        type="STOCK",
        risk_level="HIGH",
        liquidity_deadline=2,
        description="Uma das maiores instituições financeiras do Brasil."
    )
    
    Investment.objects.create(
        name="Petrobras",
        ticker="PETR4.SA",
        type="STOCK",
        risk_level="HIGH",
        liquidity_deadline=2,
        description="Empresa de capital aberto que atua no setor de energia."
    )
    
    # FIIs (Com Ticker)
    Investment.objects.create(
        name="Maxi Renda FII",
        ticker="MXRF11.SA",
        type="FII",
        risk_level="MEDIUM",
        liquidity_deadline=2,
        description="Fundo Imobiliário de Papel com grande liquidez."
    )

if __name__ == "__main__":
    seed()
    print("Database seeded with mock assets.")
