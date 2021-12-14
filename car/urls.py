from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from car import views


router = DefaultRouter()
router.register('carbrands', views.CarbrandViewSet)

app_name = 'car'

urlpatterns = [
    path('', include(router.urls))
]