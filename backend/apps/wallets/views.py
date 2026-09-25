from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Wallet
from .serializers import WalletSerializer

class WalletRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletSerializer

    def get_object(self):
        # Retorna a carteira do usuário logado.
        # Devido ao signal, ela sempre existirá.
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        return wallet
