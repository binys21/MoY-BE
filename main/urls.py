from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('black/<str:category>/', BlackListView.as_view()),
    path('white/<str:category>/', WhiteListView.as_view()),
    path('black/search', BlackPostSearchView.as_view()),
    path('white/search', WhitePostSearchView.as_view()),
    path('black/<int:post_id>/', BlackPostDetailView.as_view()),
    path('white/<int:post_id>/', WhitePostDetailView.as_view()),
    path('black/<int:post_id>/delete/', BlackPostDeleteView.as_view()),
    path('white/<int:post_id>/delete/', WhitePostDeleteView.as_view()),
    path('black/mypage', BlackMypageView.as_view()),
    path('white/mypage', WhiteMypageView.as_view()),

]



