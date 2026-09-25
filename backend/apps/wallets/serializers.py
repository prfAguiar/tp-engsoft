from rest_framework import serializers
from .models import Wallet, WalletItem
from apps.investments.models import Investment

class WalletItemSerializer(serializers.ModelSerializer):
    investment_name = serializers.CharField(source='investment.name', read_only=True)
    investment_type = serializers.CharField(source='investment.type', read_only=True)

    class Meta:
        model = WalletItem
        fields = ('id', 'investment', 'investment_name', 'investment_type', 'amount')

class WalletSerializer(serializers.ModelSerializer):
    items = WalletItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'total_amount', 'items', 'updated_at')
        read_only_fields = ('id', 'items', 'updated_at')
