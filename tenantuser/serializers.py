from rest_framework import serializers
from .models import TenantUser


class TenantUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "role_type",
            "role_id",
            "password",
            "account_status",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }


class TenantUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        exclude = ["password"]
