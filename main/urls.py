from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('main/black/<str:category>/', BlackListView.as_view()),
    path('main/white/<str:category>/', WhiteListView.as_view()),
    path('main/black/search', BlackPostSearchView.as_view()),
    path('main/white/search', WhitePostSearchView.as_view()),
    path('main/black/<int:post_id>/', BlackPostDetailView.as_view()),
    path('main/white/<int:post_id>/', WhitePostDetailView.as_view()),
    path('main/black/<int:post_id>/delete/', BlackPostDeleteView.as_view()),
    path('main/white/<int:post_id>/delete/', WhitePostDeleteView.as_view()),

]



