from rest_framework import viewsets
from rest_framework import authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.models import Carbrand, Carmodel

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

    def perform_create(self, serializer):
        """Create a new carbrand"""
        serializer.save(user=self.request.user)


class CarmodelViewSet(viewsets.ModelViewSet):
    """Manage carmodel in the database"""
    serializer_class = serializers.CarmodelSerializer
    queryset = Carmodel.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the carmodels for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new carmodel"""
        serializer.save(user=self.request.user)