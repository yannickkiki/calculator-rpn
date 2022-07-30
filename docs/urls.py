from django.urls import path
from django.views.generic import TemplateView

from rest_framework import renderers
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path(
        "openapi.yaml",
        get_schema_view(
            title="RPN Calculator API Documentation",
            renderer_classes=[renderers.OpenAPIRenderer],
        ),
        name="openapi-schema-yaml",
    ),
    path(
        "",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema-yaml"},
        ),
        name="swagger-ui",
    ),
]
