from django.urls import path, include
from rest_framework.routers import DefaultRouter
from activities.api import *

router = DefaultRouter()
router.register(r'activities', ActivityViewSet)

api_urls = ([
    path('', include(router.urls))
] , 'activities')
