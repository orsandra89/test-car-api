from django.urls import path, include
from rest_framework import urlpatterns, viewsets
from rest_framework.routers import DefaultRouter

from car import views


router = DefaultRouter()
router.register('carbrands', views.CarbrandViewSet)
router.register('carmodels', views.CarmodelViewSet)
router.register('carobjects', views.CarobjectViewSet)

app_name = 'car'

urlpatterns = [
    path('', include(router.urls))
]