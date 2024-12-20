from django.urls import path
from .views import *


app_name = 'home'

urlpatterns = [
    path('black/', BlackHomeView.as_view()),
    path('white/', WhiteHomeView.as_view()),
    # path('black/post/', BlackPostView.as_view()),
    path('white/post/', WhitePostView.as_view()),
    path('black/search/history/', BlackHistoryView.as_view()),
    path('white/search/history/', WhiteHistoryView.as_view()),
    path('img/', ImgSearch.as_view()),
]