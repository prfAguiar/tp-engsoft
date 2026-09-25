from django.urls import path
from .views import InvestmentSuggestionView, ProjectionSimulationView, InvestmentCatalogView

urlpatterns = [
    path('projection/', ProjectionSimulationView.as_view(), name='investment-projection'),
    path('suggest/', InvestmentSuggestionView.as_view(), name='investment-suggestion'),
    path('catalog/', InvestmentCatalogView.as_view(), name='investment-catalog'),
]
