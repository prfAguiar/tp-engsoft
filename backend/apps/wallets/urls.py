from django.urls import path
from .views import WalletRetrieveUpdateView

urlpatterns = [
    path('', WalletRetrieveUpdateView.as_view(), name='wallet-detail'),
]
