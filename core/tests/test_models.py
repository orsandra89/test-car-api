from django.test import TestCase
from django.contrib.auth import get_user, get_user_model

from core import models
from core.models import Carbrand, Carmodel


def sample_carbrand(user, brandname='BMW', country='Germany'):
    """Create and return sample carbrand"""
    return Carbrand.objects.create(user=user, brandname=brandname, country=country)

def sample_carmodel(user, modelname='X5', modelyear='2020', modelbodystyle='sedan'):
    """Create and return sample carmodel"""
    return Carmodel.objects.create(user=user, modelname=modelname, modelyear=modelyear, modelbodystyle=modelbodystyle)

def sample_user(email='test123123123@gmail.com', password='test123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email=email, password=password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = 'Test123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user is normilized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email = email
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises eror"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'testadmin@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_carbrand_str(self):
        """Test the carbrand string representation"""
        carbrand = models.Carbrand.objects.create(
            user = sample_user(),
            brandname = "BMW",
            country = "Germany"
        )
        
        self.assertEqual(str(carbrand), carbrand.brandname)

    def test_carmodel_str(self):
        """Test the carmodel string representation"""
        carmodel = models.Carmodel.objects.create(
            user = sample_user(),
            modelname = "E 200",
            modelyear = "2008",
            modelbodystyle = "sedan"
        )

        self.assertEqual(str(carmodel), carmodel.modelname)

    def test_carobject_str(self):
        """Test the carobject string representation"""
        user = sample_user()
        carbrand = sample_carbrand(user = user)
        carmodel = sample_carmodel(user = user)
        carobject = models.Carobject.objects.create(
            carbrand = carbrand,
            carmodel = carmodel,
            user = user,
            price = 10.0,
            mileage = 1000.0,
            exteriorcolor = 'white',
            interiorcolor = 'white',
            fuel = 'gas',
            transmission = 'mechanic',
            engineL = '2.0L',
            sale = 'True'
        )
        self.assertEqual(str(carobject), f'{carbrand} {carmodel}')