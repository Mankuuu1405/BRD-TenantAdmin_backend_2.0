from rest_framework import serializers
from .models import Disbursement  # only the actual model

class DisbursementSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='mandate.bank_name', read_only=True)
    account_number = serializers.CharField(source='mandate.account_number', read_only=True)
    ifsc_code = serializers.CharField(source='mandate.ifsc_code', read_only=True)

    class Meta:
        model = Disbursement
        fields = '__all__'
