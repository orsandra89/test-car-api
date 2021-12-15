from django.db.models import fields
from rest_framework import serializers

from core.models import Carbrand, Carmodel, Carobject


class CarbrandSerializer(serializers.ModelSerializer):
    """Serialize a carbrand"""

    class Meta:
        model = Carbrand
        fields = ('id', 'brandname', 'country')
        read_only_fields = ('id',)


class CarmodelSerializer(serializers.ModelSerializer):
    """Serialize a carmodel"""

    class Meta:
        model = Carmodel
        fields = ('id', 'modelname', 'modelyear', 'modelbodystyle')
        read_only_fields = ('id',)


class CarobjectSerializer(serializers.ModelSerializer):
    """Serialize a carobject"""
    carbrand = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Carbrand.objects.all()
    )
    carmodel = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = Carmodel.objects.all()
    )

    class Meta:
        model = Carobject
        fields = (
            'id', 'carbrand', 'carmodel', 'price', 'mileage',
            'exteriorcolor', 'interiorcolor', 'fuel', 'transmission',
            'engineL', 'sale'
        )
        read_only_fields = ('id',)


class CarobjectDetailSerializer(CarobjectSerializer):
    """Serialize a carobject detail"""
    carmodels = CarmodelSerializer(many=True, read_only=True)
    carbrands = CarbrandSerializer(many=True, read_only=True)