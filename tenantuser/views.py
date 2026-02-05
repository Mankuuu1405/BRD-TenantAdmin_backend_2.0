from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    TenantUserCreateSerializer,
    TenantUserListSerializer
)
from .services import TenantUserService


class TenantUserCreateView(APIView):
    """
    CREATE USER (Add New User screen)
    """

    def post(self, request):
        serializer = TenantUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = TenantUserService.create_user(serializer.validated_data)

        return Response(
            {
                "message": "User created successfully",
                "user_id": user.id
            },
            status=status.HTTP_201_CREATED
        )


class TenantUserListView(APIView):
    """
    LIST USERS (Tenant wise)
    """

    def get(self, request):

        users = TenantUserService.list_users(tenant_id)
        serializer = TenantUserListSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
