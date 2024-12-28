from Bankist.models import Bankist,TransactionHistory
from rest_framework import serializers

class TransferSerializer(serializers.Serializer):
  amount = serializers.DecimalField(max_digits=120,decimal_places=2)
  reciver_account_number = serializers.CharField(max_length=14)
  pin = serializers.CharField(max_length=120)
  def validate(self, attrs):
    if not len(attrs['reciver_account_number']) == 14:
      raise serializers.ValidationError("account_number digits must be 14")
    return attrs
  def validate_amount(self,value):
    if value <= 0:
      raise serializers.ValidationError("Amount must be greater than zero.")
    return value
  
  
class DepositSeriaizer(serializers.Serializer):
  amount = serializers.DecimalField(max_digits=120,decimal_places=2)
  pin = serializers.CharField(max_length=120)
  def validate(self, attrs):
    if attrs['amount'] <= 0:
      raise serializers.ValidationError("You can't deposit this amount")
    return attrs


class TransactionHistorySerialier(serializers.ModelSerializer):
  class Meta:
    model = TransactionHistory
    fields = '__all__'


class BankistSerializer(serializers.ModelSerializer):
  transaction_history = TransactionHistorySerialier(many=True,read_only=True)
  class Meta:
    model = Bankist
    fields = ('account_number','user_profile','balance','pin','transaction_history')
    read_only_fields = ('account_number',)
# "50001137910872"

