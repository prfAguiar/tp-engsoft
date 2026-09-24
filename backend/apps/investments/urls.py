from django.urls import path
from .views import ProjectionSimulationView

urlpatterns = [
    path('projection/', ProjectionSimulationView.as_view(), name='investment-projection'),
]
