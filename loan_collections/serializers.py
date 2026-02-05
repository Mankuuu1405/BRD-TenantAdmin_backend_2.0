from rest_framework import serializers
from .models import Delinquency


class DelinquencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delinquency
        fields = "__all__"
