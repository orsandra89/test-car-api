from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import test
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Carmodel

from car.serializers import CarmodelSerializer


CARMODEL_URL = reverse('car:carmodel-list')


def sample_carmodel(user, **params):
    """Create and return a sample carmodel"""
    defaults = {
        'modelname': 'a8',
        'modelyear': "2006",
        'modelbodystyle': 'sedan'
    }
    defaults.update(params)

    return Carmodel.objects.create(user=user, **defaults)


class PublicCarbrandApiTests(TestCase):
    """Test unauthenticated car API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authenticated is required"""
        res = self.client.get(CARMODEL_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCarbrandApiTests(TestCase):
    """Test unauthenticated car API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'test123'
        )
        self.client.force_authenticate(self.user)

    def test_retreive_carmodel(self):
        """Test retrieving a list of carbrand"""
        sample_carmodel(user=self.user)
        sample_carmodel(user=self.user)

        res = self.client.get(CARMODEL_URL)

        carbrands = Carmodel.objects.all().order_by('id')
        serializer = CarmodelSerializer(carbrands, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_carmodels_limited_to_user(self):
        """Test retrieving carbmodels for user"""
        user2 = get_user_model().objects.create_user(
            'test2@gmail.com',
            'test123'
        )
        sample_carmodel(user=user2)
        sample_carmodel(user=self.user)

        res = self.client.get(CARMODEL_URL)

        carbrands = Carmodel.objects.filter(user=self.user)
        serializer = CarmodelSerializer(carbrands, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_carmodel(self):
        """Test creating carmodel"""
        payload = {
            'modelname': "a8",
            'modelyear': 2006,
            'modelbodystyle': 'sedan'
        }
        res = self.client.post(CARMODEL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        carbrand = Carmodel.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(carbrand, key))