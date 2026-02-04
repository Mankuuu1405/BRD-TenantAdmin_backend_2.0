from rest_framework import serializers
from .models import ThirdPartyUser

class ThirdPartyUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = ThirdPartyUser
        fields = "__all__"

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = ThirdPartyUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
