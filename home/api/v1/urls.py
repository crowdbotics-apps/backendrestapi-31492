from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet,
    PlanViewSet,
    SubscriptionViewSet,
    AppViewSet,
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("plans", PlanViewSet, basename="plans")
router.register("subscriptions", SubscriptionViewSet, basename="subscriptions")
router.register("apps", AppViewSet, basename="apps")

urlpatterns = [
    path("", include(router.urls)),
]
