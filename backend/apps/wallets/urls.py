from django.urls import path
from .views import WalletRetrieveUpdateView, WalletItemCreateView, WalletItemDestroyView

urlpatterns = [
    path('', WalletRetrieveUpdateView.as_view(), name='wallet-detail'),
    path('items/', WalletItemCreateView.as_view(), name='wallet-item-create'),
    path('items/<int:pk>/', WalletItemDestroyView.as_view(), name='wallet-item-delete'),
]
