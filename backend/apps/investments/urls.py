from django.urls import path
from .views import InvestmentSuggestionView, ProjectionSimulationView

urlpatterns = [
    path('projection/', ProjectionSimulationView.as_view(), name='investment-projection'),
    path('suggest/', InvestmentSuggestionView.as_view(), name='investment-suggestion'),
]
