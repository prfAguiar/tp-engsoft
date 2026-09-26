from rest_framework import serializers
from .models import Wallet, WalletItem
from apps.investments.models import Investment

class WalletItemSerializer(serializers.ModelSerializer):
    investment_name = serializers.CharField(source='investment.name', read_only=True)
    investment_type = serializers.CharField(source='investment.type', read_only=True)
    profitability_estimate = serializers.SerializerMethodField()

    class Meta:
        model = WalletItem
        fields = ('id', 'investment', 'investment_name', 'investment_type', 'profitability_estimate', 'amount')

    def get_profitability_estimate(self, obj):
        if obj.investment.profitability:
            return float(obj.investment.profitability)
        # Fallbacks for variable income
        if obj.investment.type == 'STOCK':
            return 12.0
        elif obj.investment.type == 'FII':
            return 9.0
        return 10.5

class WalletSerializer(serializers.ModelSerializer):
    items = WalletItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'total_amount', 'items', 'updated_at')
        read_only_fields = ('id', 'items', 'updated_at')
