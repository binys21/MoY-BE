from django.shortcuts import render, redirect
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
import graduation
from .models import *
from .serializers import *
import requests
import math
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
#from .pagination import PaginationHandlerMixin
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


# # Create your views here.
KAKAO_CLIENT_ID = getattr(graduation.settings.base, 'KAKAO_CLIENT_ID')
KAKAO_APP_ID = getattr(graduation.settings.base, 'KAKAO_APP_ID')
KAKAO_CLIENT_SECRET_KEY = getattr(graduation.settings.base, 'KAKAO_CLIENT_SECRET_KEY')
KAKAO_REDIRECT_URI = getattr(graduation.settings.base, 'KAKAO_REDIRECT_URI')
KAKAO_USERNAME = getattr(graduation.settings.base, 'KAKAO_USERNAME')
KAKAO_PASSWORD = getattr(graduation.settings.base, 'KAKAO_PASSWORD')
KAKAO_LOGIN_URI = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URI = "https://kauth.kakao.com/oauth/token"
KAKAO_PROFILE_URI = "https://kapi.kakao.com/v2/user/me"


class SignUpView(views.APIView):
    authentication_classes = ()
    def post(self,request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user, access, refresh = serializer.save()
            returndata={"id":user.id,"nickname":user.nickname,"access_token":access, "refresh_token":refresh}
            return Response({'message':'회원가입 성공','data':returndata}, status=HTTP_201_CREATED)
        return Response({'message':'회원가입 실패','error':serializer.errors},status=HTTP_400_BAD_REQUEST)
    
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.validated_data}, status=HTTP_200_OK)
        return Response({'message': "로그인 실패", 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
class DuplicateUsernameView(views.APIView):
    def post(self, request):
        return Response({'message': "아이디 중복 확인 성공","data":{"duplicate":User.objects.filter(username=request.data['username']).exists()}}, status=HTTP_200_OK)

class KakaoLoginView(views.APIView):
    def get(self, request):
        uri = f"{KAKAO_LOGIN_URI}?client_id={KAKAO_CLIENT_ID}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code"
        
        res = redirect(uri)
        # res = requests.get(uri)
        print(res.get("access_token"))
        return res

class KakaoCallbackView(views.APIView):
    def get(self, request):         
        # access_token 발급 요청
        code = request.GET.get('code')
        if not code:
            return Response(status=HTTP_400_BAD_REQUEST)

        request_data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CLIENT_ID,
            'redirect_uri': KAKAO_REDIRECT_URI,
            'client_secret': KAKAO_CLIENT_SECRET_KEY,
            'code': code,
        }
        token_headers = {
            'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        token_res = requests.post(KAKAO_TOKEN_URI, data=request_data, headers=token_headers)

        token_json = token_res.json()
        access_token = token_json.get('access_token')

        if not access_token:
            return Response(status=HTTP_400_BAD_REQUEST)
        access_token = f"Bearer {access_token}" \

        # kakao 회원정보 요청
        auth_headers = {
            "Authorization": access_token,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        user_info_res = requests.post(KAKAO_PROFILE_URI, headers=auth_headers)
        user_info_json = user_info_res.json()
        social_id = str(user_info_json.get('id'))

        # 회원가입 및 로그인 처리 
        try:   
            user_in_db = User.objects.get(username=KAKAO_USERNAME+social_id) 
            # kakao계정 아이디가 이미 가입한거라면
            # 서비스에 rest-auth 로그인
            data={'username':KAKAO_USERNAME+social_id,'password':KAKAO_PASSWORD}
            serializer = KakaoLoginSerializer(data=data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data['exist'] = True
                return Response({'message': "카카오 로그인 성공", 'data': validated_data}, status=HTTP_200_OK)
            return Response({'message': "카카오 로그인 실패", 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:   
            return Response({'message':'카카오 회원가입 진행','data':{"exist":False,"username":social_id}}, status=HTTP_201_CREATED)

class KakaoSignupView(views.APIView):
    def post(self, request):  
        request_data=request.data
        request_data['username']=KAKAO_USERNAME+request.data['username']
        request_data['password']=KAKAO_PASSWORD
        serializer = SignUpSerializer(data=request_data)
        if serializer.is_valid():
            user, access, refresh = serializer.save()
            data={"id":user.id,"nickname":user.nickname,"access_token":access,"refresh_token": refresh}
            return Response({'message':'닉네임 등록, 카카오 회원가입 완료','data':data}, status=HTTP_201_CREATED)
        return Response({'message':'카카오','error':serializer.errors},status=HTTP_400_BAD_REQUEST)

class TokenRefreshView(views.APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh", None)

        if not refresh_token:
            return Response(
                {"message": str(e)},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            # Refresh token을 통해 새로운 access token 생성
            token = RefreshToken(refresh_token)
            new_access_token = token.access_token

            # 커스터마이즈된 반환 데이터 구조
            return Response(
                {
                    "message": "access token 업데이트",
                    "data": {
                        "access_token": str(new_access_token)
                    },
                },
                status=HTTP_200_OK,
            )

        except TokenError as e:
            return Response(
                {
                    "message": "유효하지 않거나 만료된 refresh 토큰입니다"
                },
                status=HTTP_401_UNAUTHORIZED,
            )
        

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        refresh_token = self.request.data.get('refresh_token')

        if not refresh_token:
            return Response({"message": "Refresh token이 필요합니다."}, status=HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            # 블랙리스트 처리 완료 후 응답
            return Response({"message": "로그아웃 성공"}, status=HTTP_200_OK)

        except InvalidToken:
            return Response({"message": "유효하지 않거나 만료된 refresh 토큰입니다"}, status=HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"message": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)