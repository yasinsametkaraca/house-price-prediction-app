from django.urls import path
from .views import HouseList

urlpatterns = [
    path('', HouseList.as_view()),
]