from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'accounts'

urlpatterns = [
        path('signup/',csrf_exempt(SignUpView.as_view())),
        path('login/',LoginView.as_view()),
        path('duplicate/',DuplicateUsernameView.as_view()),
        path('kakao/', KakaoLoginView.as_view()),
        path('kakao/callback/',KakaoCallbackView.as_view()),
        path('kakao/nickname/', KakaoSignupView.as_view()),
]