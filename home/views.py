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

class BlackHomeView(APIView):
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
    


class WhiteHomeView(APIView):
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
    