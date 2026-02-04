from rest_framework import serializers
from .models import CreditScoreRule, NegativeArea

class CreditScoreRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditScoreRule
        exclude = ('tenant',)
        
class NegativeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NegativeArea
        exclude = ('tenant',)
