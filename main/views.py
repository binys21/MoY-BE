from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *

class PostListPagination(PageNumberPagination):
    page_size = 10  


class BlackListView(APIView):
    def get(self, request, category):
        posts = Black.objects.filter(category=category).order_by('-id')

        paginator = PostListPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = BlackSerializer(paginated_posts, many=True)

        paginated_response = paginator.get_paginated_response(serializer.data).data

        return Response({
            "message": "블랙 분야별 목록 조회 성공",
            "data": paginated_response},status=status.HTTP_200_OK
        )

class WhiteListView(APIView):
    def get(self,request,category):
        posts=White.objects.filter(category=category).order_by('-id')
        paginator=PostListPagination()
        paginated_posts = paginator.paginate_queryset(posts,request)
        serializer=WhiteSerializer(paginated_posts,many=True)

        paginated_response = paginator.get_paginated_response(serializer.data).data

        return Response({
            "message":"화이트 분야별 목록 조회 성공",
            "data": paginated_response},status=status.HTTP_200_OK)
    

class BlackPostSearchView(APIView):
    def get(self,request):
        try:
            category=request.query_params.get('category',None)
            name=request.query_params.get('name',None)
            nickname=request.query_params.get('nickname',None)

            posts=Black.objects.all()
            if category:
                posts=posts.filter(category=category)
            if name:
                posts=posts.filter(name__icontains=name)

            if nickname:
                posts=posts.filter(user__nickname__icontain=nickname)
            posts=posts.order_by('-id')

            paginator=PostListPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = BlackSerializer(paginated_posts, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data).data
            
            if not posts.exists():
                return Response(
                        {"message": "검색 결과가 없습니다", "data": []},
                        status=status.HTTP_404_NOT_FOUND
                    )

            return Response(
                {"message": "검색 성공","data": paginated_response},
                status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"message":"잘못된 요청입니다. 파라미터를 확인해주세요"},
                status=status.HTTP_400_BAD_REQUEST
            )    

class WhitePostSearchView(APIView):
    def get(self,request):
        try:
            category=request.query_params.get('category',None)
            name=request.query_params.get('name',None)
            nickname=request.query_params.get('nickname',None)

            posts=White.objects.all()
            if category:
                posts=posts.filter(category=category)
            if name:
                posts=posts.filter(name__icontains=name)

            if nickname:
                posts=posts.filter(user__nickname__icontain=nickname)
            posts=posts.order_by('-id')

            paginator=PostListPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = WhiteSerializer(paginated_posts, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data).data
            
            if not posts.exists():
                return Response(
                        {"message": "검색 결과가 없습니다", "data": []},
                        status=status.HTTP_404_NOT_FOUND
                    )

            return Response(
                {"message": "검색 성공","data": paginated_response},
                status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"message":"잘못된 요청입니다. 파라미터를 확인해주세요"},
                status=status.HTTP_400_BAD_REQUEST
            )    
        
class BlackPostDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,post_id):
        try:
            post=Black.objects.get(id=post_id)
        except Black.DoesNotExist:
            return Response({"message": "게시물이 존재하지 않습니다."}, 
                            status=status.HTTP_404_NOT_FOUND)
        serializer=BlackPostDetailSerializer(post,context={'request':request})

        return Response({
            "message": "블랙 포스트 상세 정보 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    
class WhitePostDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,post_id):
        try:
            post=White.objects.get(id=post_id)
        except White.DoesNotExist:
            return Response({"message": "게시물이 존재하지 않습니다."}, 
                            status=status.HTTP_404_NOT_FOUND)
        serializer=WhitePostDetailSerializer(post,context={'request':request})

        return Response({
            "message": "화이트 포스트 상세 정보 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)