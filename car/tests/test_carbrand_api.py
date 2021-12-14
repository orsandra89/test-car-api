from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import test
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Carbrand

from car.serializers import CarbrandSerializer


CARBRANDS_URL = reverse('car:carbrand-list')


def sample_carbrand(user, **params):
    """Create and return a sample carbrand"""
    defaults = {
        'brandname': 'BMW',
        'country': "Germany"
    }
    defaults.update(params)

    return Carbrand.objects.create(user=user, **defaults)


class PublicCarbrandApiTests(TestCase):
    """Test unauthenticated car API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authenticated is required"""
        res = self.client.get(CARBRANDS_URL)

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

    def test_retreive_carbrand(self):
        """Test retrieving a list of carbrand"""
        sample_carbrand(user=self.user)
        sample_carbrand(user=self.user)

        res = self.client.get(CARBRANDS_URL)

        carbrands = Carbrand.objects.all().order_by('id')
        serializer = CarbrandSerializer(carbrands, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_carbrands_limited_to_user(self):
        """Test retrieving carbrands for user"""
        user2 = get_user_model().objects.create_user(
            'test2@gmail.com',
            'test123'
        )
        sample_carbrand(user=user2)
        sample_carbrand(user=self.user)

        res = self.client.get(CARBRANDS_URL)

        carbrands = Carbrand.objects.filter(user=self.user)
        serializer = CarbrandSerializer(carbrands, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)