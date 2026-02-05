from rest_framework.routers import DefaultRouter
from .views import (
    AccessRuleViewSet,
    WorkflowRuleViewSet,
    ValidationRuleViewSet,
    AssignmentRuleViewSet,
    SecurityRuleViewSet,
)

router = DefaultRouter()
router.register("access-rules", AccessRuleViewSet)
router.register("workflow-rules", WorkflowRuleViewSet)
router.register("validation-rules", ValidationRuleViewSet)
router.register("assignment-rules", AssignmentRuleViewSet)
router.register("security-rules", SecurityRuleViewSet)

urlpatterns = router.urls
