from rest_framework import viewsets
from rest_framework import authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.models import Carbrand, Carmodel, Carobject

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


class CarobjectViewSet(viewsets.ModelViewSet):
    """Manage carobjects in the database"""
    serializer_class = serializers.CarobjectSerializer
    queryset = Carobject.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def _params_to_ints(self, qs):
    #     """Convert a list of string IDs to a list of integers"""
    #     return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        # """Retrieve the carobjects for the authenticated user"""
        # carbrands = self.request.query_params.get('carbrands')
        # carmodels = self.request.query_params.get('carmodels')
        # queryset = self.queryset
        # if carbrands:
        #     carbrand_ids = self._params_to_ints(carbrands)
        #     queryset = queryset.filter(carbrands__id__in=carbrand_ids)
        # if carmodels:
        #     carmodel_ids = self._params_to_ints(carmodels)
        #     queryset = queryset.filter(carmodels__id__in=carmodel_ids)

        return Carobject.objects.filter(user=self.request.user)

    # def get_serializer_class(self):
    #     """Return appropriate serializer class"""
    #     if self.action == 'retrieve':
    #         return serializers.CarobjectDetailSerializer

    #     return self.serializer_class

    def perform_create(self, serializer):
        """Create a new carobject"""
        serializer.save(user=self.request.user)