from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('main/black/<str:category>/', BlackListView.as_view()),
    path('main/white/<str:category>/', BlackListView.as_view())
]



