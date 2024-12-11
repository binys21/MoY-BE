from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from main.models import *
from accounts.models import User
from rest_framework import status
from django.db.models import Count
import random
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from .storages import FileUpload, s3_client
import os
import graduation

bucket_name = getattr(graduation.settings.base, 'AWS_STORAGE_BUCKET_NAME')

class BlackHomeView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
        
    def get(self, request):
        if request.user.is_authenticated:
            message = "로그인한 사용자 블랙 메인화면 조회 성공"
            posts = Black.objects.filter(user=request.user).order_by('?')
            nickname=request.user.nickname
        else:
            message = "비로그인 사용자 블랙 메인화면 조회 성공"
            eligible_users = (
                Black.objects.values('user')
                .annotate(black_count=Count('id'))
                .filter(black_count__gte=5)
                .values_list('user', flat=True)
            )
            
            if eligible_users:
                random_user_id = random.choice(list(eligible_users))
                posts = Black.objects.filter(user=random_user_id).order_by('?')
                user=get_object_or_404(User, id=random_user_id)
                nickname=user.nickname
            else:
                posts = Black.objects.none()
                nickname=""

        serializer = BlackSerializer(posts, many=True)

        
        return Response({
            "message": message,
            "data": {
                "nickname":nickname,
                "posts": serializer.data
            }
        }, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        file = request.FILES.get('img') or request.data.get('img')
        if isinstance(file, str):
            data = request.data.copy()
            data['user'] = request.user.id
            serializer = BlackPostSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()
                response_data = serializer.data 
                response_data['nickname'] = request.user.nickname 
                return Response({
                    "message": "블랙 등록 성공(이미지 링크)",
                    "data": response_data
                }, status=status.HTTP_201_CREATED)
        data = request.data.copy()
        data.pop('img')
        data['user'] = request.user.id
        data['img'] = "tmp"
        serializer = BlackPostSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()

            # S3에 파일 업로드
            _, ext = os.path.splitext(file.name)  # 확장자 추출
            folder = f"{request.user.id}_{request.user.username}_img/black/{instance.id}{ext}"
            file_url = FileUpload(s3_client).upload(file, folder)

            instance.img = file_url
            instance.save()

            response_data = serializer.data 
            response_data['nickname'] = request.user.nickname 
            
            return Response({
                    "message": "블랙 등록 성공(이미지 파일)",
                    "data": response_data
                }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "블랙 등록 실패",
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class WhiteHomeView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    def get(self, request):
        if request.user.is_authenticated:
            message = "로그인한 사용자 화이트 메인화면 조회 성공"
            posts = White.objects.filter(user=request.user).order_by('?')
            nickname=request.user.nickname
        else:
            message = "비로그인 사용자 화이트 메인화면 조회 성공"
            eligible_users = (
                White.objects.values('user')
                .annotate(white_count=Count('id'))
                .filter(white_count__gte=5)
                .values_list('user', flat=True)
            )
            
            if eligible_users:
                random_user_id = random.choice(list(eligible_users))
                posts = White.objects.filter(user=random_user_id).order_by('?')
                user=get_object_or_404(User, id=random_user_id)
                nickname=user.nickname
            else:
                posts = White.objects.none()
                nickname=""

        serializer = WhiteSerializer(posts, many=True)

        
        return Response({
            "message": message,
            "data": {
                "nickname":nickname,
                "posts": serializer.data
            }
        }, status=status.HTTP_200_OK)
    def post(self, request, format=None):
        file = request.FILES.get('img') or request.data.get('img')
        if isinstance(file, str):
            data = request.data.copy()
            data['user'] = request.user.id
            serializer = WhitePostSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()
                response_data = serializer.data 
                response_data['nickname'] = request.user.nickname 
                return Response({
                    "message": "화이트 등록 성공(이미지 링크)",
                    "data": response_data
                }, status=status.HTTP_201_CREATED)
        data = request.data.copy()
        data.pop('img')
        data['user'] = request.user.id
        data['img'] = "tmp"
        serializer = WhitePostSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()

            # S3에 파일 업로드
            _, ext = os.path.splitext(file.name)  # 확장자 추출
            folder = f"{request.user.id}_{request.user.username}_img/white/{instance.id}{ext}"
            file_url = FileUpload(s3_client).upload(file, folder)

            instance.img = file_url
            instance.save()

            response_data = serializer.data 
            response_data['nickname'] = request.user.nickname 
            
            return Response({
                    "message": "화이트 등록 성공(이미지 파일)",
                    "data": response_data
                }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "화이트 등록 실패",
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)