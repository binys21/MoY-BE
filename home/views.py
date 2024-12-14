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

from graduation.settings.base import redis_client
def get_black_search_history(user_id):
    redis_key = f"user:{user_id}:black"
    return redis_client.lrange(redis_key, 0, -1)  # 리스트의 모든 요소 반환
def get_white_search_history(user_id):
    redis_key = f"user:{user_id}:white"
    return redis_client.lrange(redis_key, 0, -1)

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
        try:
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
        except Exception as e:
                print(f"Error: {e}")
                return Response({
                    "message": "서버 내부 오류가 발생했습니다.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
        try:
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
        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BlackHistoryView(APIView):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                user_id = request.user.username
                search_history = get_black_search_history(user_id)
                formatted_history = [{"keyword": keyword} for keyword in search_history]
                
                return Response({
                    "message": "최근 검색어 조회 성공",
                    "data": formatted_history
                }, status=200)
            else:
                return Response({
                    "message": "로그인하지 않은 사용자입니다",
                    "data": []
                }, status=200)
            
        except Exception as e:
            return Response({
                "message": "최근 검색어 조회 실패",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class WhiteHistoryView(APIView):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                user_id = request.user.username
                search_history = get_white_search_history(user_id)
                formatted_history = [{"keyword": keyword} for keyword in search_history]
                return Response({
                    "message": "최근 검색어 조회 성공",
                    "data": formatted_history
                }, status=200)
            else:
                return Response({
                    "message": "로그인하지 않은 사용자입니다",
                    "data": []
                }, status=200)
            
        except Exception as e:
            return Response({
                "message": "최근 검색어 조회 실패",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import requests
NAVER_CLIENT_ID = getattr(graduation.settings.base, 'NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = getattr(graduation.settings.base, 'NAVER_CLIENT_SECRET')

def search_books(query, display=20, start=1, sort='sim'):
    url = "https://openapi.naver.com/v1/search/book.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,    # 검색어
        "display": display,  # 한 번에 가져올 결과 개수
        "start": start,     # 시작 위치
        "sort": sort        # 정렬 방식
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        items = response.json().get("items", [])
        results = [
                {
                    "img": item.get("image"),
                    "information": item.get("author", "")
                }
                for item in items if item.get("image")
            ]
        return results
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as e:
        print(f"Failed to parse JSON: {e}")
        return None

def search_naver_images(query, display=20, start=1, sort='sim', filter='all'):
    url = "https://openapi.naver.com/v1/search/image"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,    # 검색어
        "display": display,  # 한 번에 가져올 결과 개수
        "start": start,     # 시작 위치
        "sort": sort,       # 정렬 방식
        "filter": filter    # 이미지 필터
    }
    
    response = requests.get(url, headers=headers, params=params)
    images = [{"img": item["link"], "information": ""} for item in response.json().get("items", []) if item.get("link")]

    # 응답 확인
    if response.status_code == 200:
        return images  # JSON 결과 반환
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# 이미지 유효성 확인
def is_valid_image(url):
    try:
        response = requests.get(url, timeout=2)
        return response.status_code == 200 and "image" in response.headers.get("Content-Type", "")
    except requests.RequestException:
        return False
from concurrent.futures import ThreadPoolExecutor
def filter_valid_images(image_list):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda item: (item, is_valid_image(item["img"])), image_list))
        return [item for item, is_valid in results if is_valid]
    

class ImgSearch(APIView):
    def post(self,request):
        category = request.GET.get('category')
        keyword = request.GET.get('keyword')

        try:
            result=None
            if category == "영화":
                result = search_naver_images(keyword+" 포스터")
            elif category == "음악":
                result = search_naver_images(keyword+" 앨범 커버")
            elif category == "책":
                result = search_books(keyword)
            elif category == "유투브":
                result = search_naver_images(keyword+" youtube")
            elif category == "OTT":
                result = search_naver_images(keyword+"포스터")
            elif category == "공연":
                result = search_naver_images(keyword+"포스터")
            

            if result is None:
                Response({
                "message": f"{category} 이미지 검색 실패",
            }, status=status.HTTP_400_BAD_REQUEST)
            
            # result = filter_valid_images(result)

            return Response({
                "message": f"{category} 이미지 검색 성공",
                "data": result
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)