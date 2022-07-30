from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rpn.viewsets import StackItemViewSet

from docs.urls import urlpatterns as urlpatterns_docs

router_api = DefaultRouter()
router_api.register("rpn/stack_items", StackItemViewSet, basename="stack_items")

urlpatterns = [
    path("api/", include(router_api.urls)),
] + urlpatterns_docs
