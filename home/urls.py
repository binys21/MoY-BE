from django.urls import path
from .views import *


app_name = 'home'

urlpatterns = [
    path('black/', BlackHomeView.as_view()),
    path('white/', WhiteHomeView.as_view()),
]