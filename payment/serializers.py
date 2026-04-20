# payments/serializers.py

from rest_framework import serializers
from .models import Payment, Payout


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ['status', 'paid_at', 'transaction_id']


class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = "__all__"
        read_only_fields = ['status', 'paid_at']