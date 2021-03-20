from .views import PsicologoViewSet
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'psicologo', PsicologoViewSet)
