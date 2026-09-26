from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, WalletItem
from .serializers import WalletSerializer, WalletItemSerializer

class WalletRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletSerializer

    def get_object(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        return wallet

class WalletItemCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletItemSerializer

    def perform_create(self, serializer):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        serializer.save(wallet=wallet)

class WalletItemDestroyView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletItemSerializer

    def get_queryset(self):
        return WalletItem.objects.filter(wallet__user=self.request.user)
