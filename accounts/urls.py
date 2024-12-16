from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt import views as jwt_views

app_name = 'accounts'

urlpatterns = [
        path('signup/',csrf_exempt(SignUpView.as_view())),
        path('login/',LoginView.as_view()),
        path('duplicate/',DuplicateUsernameView.as_view()),
        path('kakao/', KakaoLoginView.as_view()),
        path('kakao/callback/',KakaoCallbackView.as_view()),
        path('kakao/nickname/', KakaoSignupView.as_view()),
        # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 액세스 토큰과 리프레시 토큰 발급
        # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # 리프레시 토큰을 사용하여 새로운 액세스 토큰 발급
        path('token/refresh/',TokenRefreshView.as_view()),
        path('logout/',LogoutView.as_view()),
        path('duplicate', DuplicateUsernameView.as_view()),
        path('health/', HealthView.health)

]