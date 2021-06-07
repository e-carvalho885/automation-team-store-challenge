from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from core import settings
from django.conf.urls.static import static

from analysis import views_front

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

from django.views.generic import TemplateView

from rest_framework.documentation import include_docs_urls


schema_view = get_swagger_view(title="Pastebin API")

urlpatterns = [url(r"^$", schema_view)]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/analysis/", include("analysis.urls")),
    path("api/api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", views_front.index),
    path("login", views_front.login_view),
    path("docs/", include_docs_urls(title="Reynolds Number Calculator API")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
