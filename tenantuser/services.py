from .models import TenantUser


class TenantUserService:

    @staticmethod
    def create_user(data):
        return TenantUser.objects.create(**data)

    @staticmethod
    def list_users(tenant_id):
        return TenantUser.objects.filter(tenant_id=tenant_id)
