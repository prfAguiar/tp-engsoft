from django.urls import path
from .views import (
    InvestmentCatalogView,
    InvestmentDetailView,
    InvestmentSuggestionView,
    ProjectionSimulationView,
)

urlpatterns = [
    path('projection/', ProjectionSimulationView.as_view(), name='investment-projection'),
    path('suggest/', InvestmentSuggestionView.as_view(), name='investment-suggestion'),
    path('catalog/', InvestmentCatalogView.as_view(), name='investment-catalog'),
    path('<int:pk>/', InvestmentDetailView.as_view(), name='investment-detail'),
]
