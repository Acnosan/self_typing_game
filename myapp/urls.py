from django.urls import path
from .views import type_game

urlpatterns = [
    path("",type_game,name='type_game'),
]
