from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
    

