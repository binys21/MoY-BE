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
from django.http import JsonResponse
from googleapiclient.discovery import build


cloudfront_url=getattr(graduation.settings.base, 'CLOUDFRONT_URL')

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
        try:
            if request.user.is_authenticated and Black.objects.filter(user=request.user).count() > 3:
                message = "로그인한 사용자 블랙 메인화면 조회 성공"
                posts = Black.objects.filter(user=request.user).order_by('?')

            else:
                message = "랜덤 블랙 메인화면 조회 성공"
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
            if request.user.is_authenticated:
                    nickname=request.user.nickname
            
            return Response({
                "message": message,
                "data": {
                    "nickname":nickname,
                    "posts": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                url=cloudfront_url+folder

                instance.img = url
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
        try:
            if request.user.is_authenticated and White.objects.filter(user=request.user).count() > 3:
                message = "로그인한 사용자 화이트 메인화면 조회 성공"
                posts = White.objects.filter(user=request.user).order_by('?')
            else:
                message = "랜덤 화이트 메인화면 조회 성공"
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
            if request.user.is_authenticated:
                    nickname=request.user.nickname
    
            
            return Response({
                "message": message,
                "data": {
                    "nickname":nickname,
                    "posts": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                url=cloudfront_url+folder

                instance.img = url
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
                    "information": item.get("author", ""),
                    "name": item.get("title")
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

def search_naver_images(query, display=15, start=1, sort='sim', filter='all'):
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
    images = [{"img": item["link"], "information": "", "name": ""} for item in response.json().get("items", []) if item.get("link")]

    # 응답 확인
    if response.status_code == 200:
        result = filter_valid_images(images)
        return result  # JSON 결과 반환
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
    

API_KEY = getattr(graduation.settings.base, 'API_KEY')
YOUTUBE_API_SERVICE_NAME =getattr(graduation.settings.base, 'YOUTUBE_API_SERVICE_NAME')
YOUTUBE_API_VERSION = getattr(graduation.settings.base, 'YOUTUBE_API_VERSION')


def search_videos(query, display=20, start=1, sort='sim'):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=display,
        type='video'
    ).execute()
    
    result = []
    for item in search_response.get('items', []):
        video_data = {
            'img': item['snippet']['thumbnails']['high']['url'],
            'information': item['snippet']['channelTitle'],
            'name': item['snippet']['title']
        }
        result.append(video_data)

    return result

TMDB_API_KEY = getattr(graduation.settings.base, 'TMDB_API_KEY')
def get_credits(media_type, item_id):
    """
    TMDb API로 작품의 감독 이름과 주요 배우 2명을 가져옴
    """
    detail_url = f"https://api.themoviedb.org/3/{media_type}/{item_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits",
        "language": "ko-KR"
    }
    try:
        response = requests.get(detail_url, params=params)
        response.raise_for_status()
        data = response.json()

        return_data="" 

        # 감독 이름
        director = None
        for crew in data.get("credits", {}).get("crew", []):
            if crew.get("job") == "Director":
                director = crew.get("name")
                break
        
        # 배우 이름 추출 (최대 2명)
        cast = [actor.get("name") for actor in data.get("credits", {}).get("cast", [])[:2]]
        if director:
            return_data = f"{director} | {', '.join(cast)}"
        else:
            return_data = ", ".join(cast)

        return return_data

    except requests.exceptions.RequestException as e:
        print(f"Error during TMDb details fetch: {e}")
        return None, []

def search_tmdb_poster(keyword, type):
    url = f"https://api.themoviedb.org/3/search/{type}"
    params = {
        "api_key": TMDB_API_KEY,
        "query": keyword,
        "language": "ko-KR"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        information=""
        
        results = [
            { #크기 다른 옵션도 가능함 일단 w500으로 설정
                "img": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}",
                "name": item.get("name") or item.get("title"),
                "id": item.get("id"),
                "media_type": item.get("media_type", "movie")
            }
            for item in data.get("results", []) if item.get("poster_path")
        ]
        enriched_results = []
        for item in results:
            information = get_credits(item["media_type"], item["id"])

            enriched_results.append({
                "img": item["img"],
                "information": information,
                "name": item["name"]
            })
        
        return enriched_results
    
    except requests.exceptions.RequestException as e:
        print(f"TMDb API Error: {e}")
        return None
    



LASTFM_API_KEY = getattr(graduation.settings.base, 'LASTFM_API_KEY')   
def search_lastfm_album_info(keyword):
    if " - " in keyword:
        parts = keyword.split(" - ")
        
        if len(parts) == 2 and parts[1] != "":  # 앨범이름&가수 같이 검색할 땐 '앨범이름 - 가수' 로 요청
            album_name, artist_name = parts[0], parts[1]
            url = f'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={LASTFM_API_KEY}&album={album_name}&artist={artist_name}&format=json'
        else:  # 가수명만 검색할 땐 ' - ' 붙여서 요청(공백도)
            artist_name = parts[0]
            url = f'http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&api_key={LASTFM_API_KEY}&artist={artist_name}&format=json'
    else:
        # 앨범이름으로 검색
        album_name = keyword
        url = f'http://ws.audioscrobbler.com/2.0/?method=album.search&api_key={LASTFM_API_KEY}&album={album_name}&format=json'
    
    response = requests.get(url)
    data = response.json()
    print("Last.fm API Response:", data)

    if 'album' in data:
        album_info = data['album']
        album_cover_url = album_info['image'][3]['#text'] if 'image' in album_info else ""
        artist = album_info['artist']
        album_title = album_info['name']

        return {
            "album_cover": album_cover_url,
            "artist": artist,
            "album_title": album_title,
        }
    elif 'topalbums' in data:
        # 가수명만 검색했을 때
        albums = data['topalbums']['album']
        return [{"album_title": album['name'], "album_cover": album['image'][3]['#text'], "artist": artist_name} for album in albums[:15]]
    else:
        print("앨범 또는 가수 정보를 찾을 수 없습니다.")
        return None

def search_lastfm_song(keyword):
    # 노래 제목 검색
    url=f'https://ws.audioscrobbler.com/2.0/?method=track.search&api_key={LASTFM_API_KEY}&track={keyword}&format=json'
    # 가수 검색
    # url=f'https://ws.audioscrobbler.com/2.0/?method=artist.search&api_key={LASTFM_API_KEY}&artist={keyword}&format=json'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        tracks = data['results']['trackmatches']['track']

        return [
            {
                "info": track.get("artist", "가수 없음"),  # 가수 이름 추출
                "name": track.get("name", "제목 없음"),    # 곡 제목 추출
                "album_cover": next(                     # 'small' 사이즈 이미지 추출
                    (img.get("#text") for img in track.get("image", []) if img.get("size") == "small"),
                    "이미지 없음"  # 이미지가 없을 경우
                )
            }
            for track in tracks[:10]  # 최대 10개 곡만 반환
        ]

    except requests.RequestException as e:
        print(f"Last.fm API Error: {e}")
        return None

SPOTIFY_CLIENT_ID = getattr(graduation.settings.base, 'SPOTIFY_CLIENT_ID')   
SPOTIFY_CLIENT_SECRET = getattr(graduation.settings.base, 'SPOTIFY_CLIENT_SECRET')   
import base64

def get_spotify_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        access_token = response.json().get("access_token")
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Spotify Token Error: {e}")
        return None


def search_spotify_song(keyword):
    access_token = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    if not access_token:
        print("Access Token 발급 실패")
        return None
    headers = {"Authorization": f"Bearer {access_token}",  "Accept-Language": "ko-KR"}
    params = {
        "q": keyword,         # 검색 키워드
        "type": "track",      # 노래 검색
        "limit": 10           # 최대 10개 반환
    }
    try:
        response = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # 노래 정보 추출
        tracks = data.get("tracks", {}).get("items", [])
        results = [
            {
                "name": track.get("name"),  # 노래 제목
                "information": ", ".join(artist["name"] for artist in track.get("artists", [])),  # 가수 이름
                "img": track.get("album", {}).get("images", [{}])[0].get("url", "이미지 없음"),  # 앨범 이미지
               
            }
            for track in tracks
        ]
        return results
    except requests.exceptions.RequestException as e:
        print(f"Spotify API Error: {e}")
        return None
    
KOPIS_API_KEY = getattr(graduation.settings.base, 'KOPIS_API_KEY')
import xml.etree.ElementTree as ET
def search_kopis(keyword):
    url=f"http://www.kopis.or.kr/openApi/restful/pblprfr?service={KOPIS_API_KEY}&shprfnm={keyword}&rows=10&cpage=1&stdate=20240101&eddate=20241212"
    try:
        response = requests.get(url)
        response.raise_for_status()

        # XML 응답 파싱
        root = ET.fromstring(response.content)
        performances = []
        for item in root.findall(".//db"):
            print(item)
            img = item.findtext("poster")  # 포스터 이미지
            name = item.findtext("prfnm")  # 공연명
            information = item.findtext("fcltynm")  # 공연 시설명
            if img and name and information:  # 필요한 정보가 모두 있는 경우만 추가
                performances.append({
                    "img": img,
                    "name": name,
                    "information": information,
                })

        if not performances:
            print("검색 결과가 없습니다.")

        return performances
    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류: {e}")
        return None
    except ET.ParseError as e:
        print(f"XML 파싱 오류: {e}")
        return None



class ImgSearch(APIView):
    def get(self,request):
        category = request.GET.get('category')
        keyword = request.GET.get('keyword')

        try:
            result=None
            if category == "영화":
                type="movie"
                result = search_tmdb_poster(keyword, type)
            elif category == "음악":
                result = search_spotify_song(keyword)
            elif category == "책":
                result = search_books(keyword)
            elif category == "유튜브":
                result = search_videos(keyword)
            elif category == "OTT":
                type="multi"
                result = search_tmdb_poster(keyword, type)
            elif category == "공연":
                result = search_kopis(keyword)
            

            if result is None:
                Response({
                "message": f"{category} 이미지 검색 실패",
            }, status=status.HTTP_400_BAD_REQUEST)
            

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
        
