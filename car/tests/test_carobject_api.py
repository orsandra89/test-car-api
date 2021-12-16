from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import serializers, status
from rest_framework.test import APIClient

from core.models import Carobject, Carbrand, Carmodel

from car.serializers import CarobjectSerializer, CarobjectDetailSerializer


CAROBJECTS_URL = reverse('car:car-list')


def detail_url(carobject_id):
    """Return carobject detail URL"""
    return reverse('car:car-detail', args=[carobject_id])


def sample_carbrand(user, name='Main'):
    """Create and return sample carbrand"""
    return Carbrand.objects.create(user=user, name=name)


def sample_carmodel(user, name='A3'):
    """Create and return sample carmodel"""
    return Carmodel.objects.create(user=user, name=name)


def sample_carobject(user, **params):
    """Create and return a sample car"""
    defaults = {
        'price': 10.0,
        'mileage': 1000.0,
        'exteriorcolor': 'white',
        'interiorcolor': 'white',
        'fuel': 'gas',
        'transmission': 'mechanic',
        'engineL': '2.0L',
        'sale': 'True'
    }
    defaults.update(params)

    return Carobject.objects.create(user=user, **defaults)


class PublicCarobjectApiTests(TestCase):
    """Test unauthenticated carobject API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(CAROBJECTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCarobjectApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_carobjects(self):
        """Test retrieving list of carobjects"""
        sample_carobject(user=self.user)
        sample_carobject(user=self.user)

        res = self.client.get(CAROBJECTS_URL)

        carobjects = Carobject.objects.all().order_by('-id')
        serializer = CarobjectSerializer(carobjects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_carobjects_limited_to_user(self):
        """Test retrieving carobject for user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'password123'
        )
        sample_carobject(user=user2)
        sample_carobject(user=self.user)

        res = self.client.get(CAROBJECTS_URL)

        carobjects = Carobject.objects.filter(user=self.user)
        serializer = CarobjectSerializer(carobjects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_carobject_detail(self):
        """Test viewing a carobject detail"""
        carobject = sample_carobject(user=self.user)
        carobject.carbrand.add(sample_carbrand(user=self.user))
        carobject.carmodel.add(sample_carmodel(user=self.user))

        url = detail_url(carobject.id)
        res = self.client.get(url)

        serializer = CarobjectDetailSerializer(carobject)
        self.assertEqual(res.data, serializer.data)

    def test_filter_carobjects_by_carbrand(self):
        """"""
        carobject1 = sample_carobject(user=self.user, fuel='gas')
        carobject2 = sample_carobject(user=self.user, fuel='diesel')
        carbrand1 = sample_carbrand(user=self.user, brandname='BMW')
        carbrand2 = sample_carbrand(user=self.user, brandname='Mercedess')
        carobject1.carbrand.add(carbrand1)
        carobject2.carbrand.add(carbrand2)
        carobject3 = sample_carobject(user=self.user, fuel='benzin')

        res = self.client.get(
            CAROBJECTS_URL,
            {'carbrand': f'{carbrand1.id},{carbrand2.id}'}
        )

        serializer1 = CarobjectSerializer(carobject1)
        serializer2 = CarobjectSerializer(carobject2)
        serializer3 = CarobjectSerializer(carobject3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_recipes_by_carmodels(self):
        """"""
        carobject1 = sample_carobject(user=self.user, fuel='gas')
        carobject2 = sample_carobject(user=self.user, fuel='diesel')
        carmodel1 = sample_carmodel(user=self.user, modelname='E200')
        carmodel2 = sample_carmodel(user=self.user, modelname='E220')
        carobject1.carmodel.add(carmodel1)
        carobject2.carmodel.add(carmodel2)
        carobject3 = sample_carobject(user=self.user, title='benzin')

        res = self.client.get(
            CAROBJECTS_URL,
            {'carmodel': f'{carmodel1.id},{carmodel2.id}'}
        )

        serializer1 = CarobjectSerializer(carobject1)
        serializer2 = CarobjectSerializer(carobject2)
        serializer3 = CarobjectSerializer(carobject3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)