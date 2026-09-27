from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Wallet, WalletItem
from .serializers import WalletSerializer, WalletItemSerializer

class WalletRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletSerializer

    def get_object(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        wallet.recalculate_total()
        return wallet

class WalletItemCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        investment = serializer.validated_data['investment']
        amount = serializer.validated_data['amount']

        item, created = WalletItem.objects.get_or_create(
            wallet=wallet,
            investment=investment,
            defaults={'amount': amount},
        )
        if not created:
            item.amount += amount
            item.save()

        output_serializer = self.get_serializer(item)
        headers = self.get_success_headers(output_serializer.data)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            headers=headers,
        )

class WalletItemDestroyView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletItemSerializer

    def get_queryset(self):
        return WalletItem.objects.filter(wallet__user=self.request.user)
