from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import StudentModelViewSet, ClaimModelViewSet, StudentExpeditureModelViewSet, StudentDailyQuotaModelViewSet, MealCardModelViewSet

router = DefaultRouter()
router.register("students", StudentModelViewSet, basename="students")
router.register("student-expeditures", StudentExpeditureModelViewSet, basename="student-expeditures")
router.register("student-daily-quotas", StudentDailyQuotaModelViewSet, basename="student-daily-quotas")
router.register("meal-cards", MealCardModelViewSet, basename="meal-cards")
router.register("claims", ClaimModelViewSet, basename="claims")


urlpatterns = [
    path("", include(router.urls)),
]