from django.contrib import auth
from rest_framework import viewsets, permissions, authentication, status
from rest_framework_simplejwt import authentication as jwt_auth
from rest_framework.response import Response


from analysis.models import Analysis
from analysis.serializers import AnalysisSerializer
from analysis.tasks import analysis_created

import logging

logger = logging.getLogger(__name__)


class AnalysisViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given analysis.

    list:
    Return a list of all the existing analyses.

    create:
    Create a new user analysis.

    update:
    Update a given analysis.

    partial_update:
    Partial Update a given analysis.

    destroy:
    Delete a given analysis.
    """

    authentication_classes = [
        jwt_auth.JWTAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Analysis.objects.all().order_by("-id")
    serializer_class = AnalysisSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        creator = self.request.user
        serializer.save(creator=creator)
        analysis_created.delay(serializer.data)
