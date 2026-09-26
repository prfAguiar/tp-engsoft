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
    
    Investment.objects.create(
        name="Vale S.A.",
        ticker="VALE3.SA",
        type="STOCK",
        risk_level="HIGH",
        liquidity_deadline=2,
        description="Uma das maiores mineradoras do mundo."
    )
    
    Investment.objects.create(
        name="WEG S.A.",
        ticker="WEGE3.SA",
        type="STOCK",
        risk_level="MEDIUM",
        liquidity_deadline=2,
        description="Gigante brasileira de motores elétricos e energia."
    )

    Investment.objects.create(
        name="Banco do Brasil",
        ticker="BBAS3.SA",
        type="STOCK",
        risk_level="MEDIUM",
        liquidity_deadline=2,
        description="Instituição financeira com forte histórico de dividendos."
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

    Investment.objects.create(
        name="CSHG Logística",
        ticker="HGLG11.SA",
        type="FII",
        risk_level="MEDIUM",
        liquidity_deadline=2,
        description="Fundo Imobiliário focado em galpões logísticos."
    )

    Investment.objects.create(
        name="Kinea Renda Imobiliária",
        ticker="KNRI11.SA",
        type="FII",
        risk_level="MEDIUM",
        liquidity_deadline=2,
        description="Fundo Imobiliário misto (galpões e lajes corporativas)."
    )
    
    # Renda Fixa Adicional
    Investment.objects.create(
        name="Tesouro IPCA+ 2035",
        type="FIXED_INCOME",
        risk_level="LOW",
        profitability=6.20,
        liquidity_deadline=0,
        description="Título público atrelado à inflação."
    )

    Investment.objects.create(
        name="LCI Banco Inter",
        type="FIXED_INCOME",
        risk_level="LOW",
        profitability=9.20,
        liquidity_deadline=90,
        description="Letra de Crédito Imobiliário isenta de Imposto de Renda."
    )

if __name__ == "__main__":
    seed()
    print("Database seeded with mock assets.")
