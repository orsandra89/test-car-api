from django.db.models import fields
from rest_framework import serializers

from core.models import Carbrand, Carmodel


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