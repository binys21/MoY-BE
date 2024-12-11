from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from django.db.models import Q

class PostListPagination(PageNumberPagination):
    page_size = 10  


class BlackListView(APIView):
    def get(self, request, category):
        try:
            posts = Black.objects.filter(category=category).order_by('-id')
            if not posts.exists():
                    return Response({
                        "message": "블랙 분야에 해당하는 데이터가 없습니다.",
                        "data": []
                    }, status=status.HTTP_200_OK)

            paginator = PostListPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = BlackSerializer(paginated_posts, many=True)
            
            total_pages = (paginator.page.paginator.count + paginator.page_size - 1) // paginator.page_size
            paginated_response = paginator.get_paginated_response(serializer.data).data
            paginated_response['total_pages'] = total_pages

            return Response({
                "message": "블랙 분야별 목록 조회 성공",
                "data": paginated_response},status=status.HTTP_200_OK
            )
        except Exception as e:
            # 예외 처리
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WhiteListView(APIView):
    def get(self,request,category):
        try:
            # 데이터 필터링 및 정렬
            posts = White.objects.filter(category=category).order_by('-id')
            if not posts.exists():
                return Response({
                    "message": "화이트 분야에 해당하는 데이터가 없습니다.",
                    "data": []
                }, status=status.HTTP_200_OK)

            paginator = PostListPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = WhiteSerializer(paginated_posts, many=True)

            total_pages = (paginator.page.paginator.count + paginator.page_size - 1) // paginator.page_size
            paginated_response = paginator.get_paginated_response(serializer.data).data
            paginated_response['total_pages'] = total_pages

            return Response({
                "message": "화이트 분야별 목록 조회 성공",
                "data": paginated_response
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class BlackPostSearchView(APIView):
    def get(self,request):
        try:
            keyword = request.GET.get('keyword', '')
            
            posts = Black.objects.filter(
                Q(category__icontains=keyword) |  # 분야 검색
                Q(name__icontains=keyword) |    # 제목 검색
                Q(user__nickname__icontains=keyword)  # 작성자 닉네임 검색
            ).order_by('-id')

            if not posts.exists():
                return Response({
                    "message": "검색 결과가 없습니다",
                    "data": []
                }, status=status.HTTP_200_OK)


            paginator=PostListPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = BlackSerializer(paginated_posts, many=True)
            total_pages = (paginator.page.paginator.count + paginator.page_size - 1) // paginator.page_size
            paginated_response = paginator.get_paginated_response(serializer.data).data
            paginated_response['total_pages'] = total_pages
            
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
            keyword = request.GET.get('keyword', '')
            
            posts = White.objects.filter(
                Q(category__icontains=keyword) |  # 분야 검색
                Q(name__icontains=keyword) |    # 제목 검색
                Q(user__nickname__icontains=keyword)  # 작성자 닉네임 검색
            ).order_by('-id')

            if not posts.exists():
                return Response({
                    "message": "검색 결과가 없습니다",
                    "data": []
                }, status=status.HTTP_200_OK)
            

            paginator=PostListPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = WhiteSerializer(paginated_posts, many=True)
            total_pages = (paginator.page.paginator.count + paginator.page_size - 1) // paginator.page_size
            paginated_response = paginator.get_paginated_response(serializer.data).data
            paginated_response['total_pages'] = total_pages
            
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
    def get(self,request,post_id):
        try:
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
        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class WhitePostDetailView(APIView):
    def get(self,request,post_id):
        try:
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
        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class BlackPostDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request,post_id):
        try:
            post=Black.objects.get(id=post_id)
        except Black.DoesNotExist:
            return Response({"message":"요청한 포스트를 찾을 수 없습니다."},
                            status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({"message": "삭제 권한이 없습니다."}, 
                            status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message": "블랙 포스트 삭제 성공!"})


class WhitePostDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request,post_id):
        try:
            post=White.objects.get(id=post_id)
        except White.DoesNotExist:
            return Response({"message":"요청한 포스트를 찾을 수 없습니다."},
                            status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response({"message": "삭제 권한이 없습니다."}, 
                            status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"message": "화이트 포스트 삭제 성공!"})


class BlackMypageView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        blacks=Black.objects.filter(user=user)
        serializer = BlackSerializer(blacks, many=True)

        response_data={
            "message": "블랙 마이페이지 조회 성공",
            "data": {
                "nickname": user.nickname, 
                "user_id": user.id,
                "content_list": serializer.data,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)
    


class WhiteMypageView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        whites=White.objects.filter(user=user)
        serializer = WhiteSerializer(whites, many=True)

        response_data={
            "message": "화이트 마이페이지 조회 성공",
            "data": {
                "nickname": user.nickname, 
                "user_id": user.id,
                "content_list": serializer.data,
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class BlackShareView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, user_id):
        try:
            try:          
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"message": "해당 유저가 존재하지 않습니다."}, 
                                status=status.HTTP_404_NOT_FOUND)
            
            posts = Black.objects.filter(user=user)
            if not posts.exists():
                    return Response({
                        "message": "해당 유저의 게시글이 없습니다",
                        "data": {
                            "nickname": user.nickname,
                            "user_id": user.id,
                            "posts": []
                        }
                    }, status=status.HTTP_200_OK)

            serializer = BlackSerializer(posts, many=True)

            return Response({
                "message": "블랙 공유페이지 조회 성공",
                "data": {
                    "nickname": user.nickname,
                    "user_id": user.id,
                    "posts": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class WhiteShareView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, user_id):
        try:
            try:          
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"message": "해당 유저가 존재하지 않습니다."}, 
                                status=status.HTTP_404_NOT_FOUND)
            
            posts = White.objects.filter(user=user)
            if not posts.exists():
                    return Response({
                        "message": "해당 유저의 게시글이 없습니다",
                        "data": {
                            "nickname": user.nickname,
                            "user_id": user.id,
                            "posts": []
                        }
                    }, status=status.HTTP_200_OK)
            serializer = WhiteSerializer(posts, many=True)

            return Response({
                "message": "화이트 공유페이지 조회 성공",
                "data": {
                    "nickname": user.nickname,
                    "user_id": user.id,
                    "posts": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error: {e}")
            return Response({
                "message": "서버 내부 오류가 발생했습니다.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)