from rest_framework import viewsets, mixins
from rest_framework import authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Carbrand

from car import serializers


class CarbrandViewSet(viewsets.ModelViewSet):
    """Manage carbrand in the database"""
    serializer_class = serializers.CarbrandSerializer
    queryset = Carbrand.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the carbrands for the authenticated user"""
        return self.queryset.filter(user=self.request.user)