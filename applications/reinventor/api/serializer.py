from rest_framework import serializers

from applications.account.models import WithdrawalRequestReinventor



# EnterEquiments serializer
class WithdrawalRequestReinventorSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequestReinventor
        fields = '__all__'