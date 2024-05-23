from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import PostListSerializer, PostSerializer, CommentSerializer
from .models import Post, Comment

@api_view(['GET', 'POST'])
def post_list(request):
    """
    모든 게시글을 조회하거나 새 게시글을 생성하는 API입니다.
    GET: 모든 게시글을 조회합니다.
    POST: 새 게시글을 생성합니다. 인증된 사용자만이 게시글을 생성할 수 있습니다.
    """
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        posts = Post.objects.all().order_by('-created_at')
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, post_pk):
    """
    특정 게시글을 조회, 수정, 삭제하는 API입니다.
    params:
    - post_pk: 조회, 수정, 삭제하려는 게시글의 primary key
    """
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if request.user.is_authenticated:
            serializer = PostSerializer(instance=post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user == post.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def user_post_list(request, username):
    """
    특정 사용자의 모든 게시글을 조회하는 API입니다.
    params:
    - username: 게시글을 조회하려는 사용자의 username
    """
    user = get_object_or_404(get_user_model(), username=username)
    user_posts = user.post_set.all()
    serializer = PostSerializer(user_posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def comment_list(request, post_pk):
    """
    특정 게시글의 모든 댓글을 조회하거나 새 댓글을 생성하는 API입니다.
    params:
    - post_pk: 댓글을 조회하거나 생성하려는 게시글의 primary key
    """
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'GET':
        comments = post.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=post, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    """
    특정 댓글을 조회, 수정, 삭제하는 API입니다.
    params:
    - comment_pk: 조회, 수정, 삭제하려는 댓글의 primary key
    """
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if request.user == comment.user:
            serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "댓글 작성자와 사용자가 다릅니다."}, status=status.HTTP_401_UNAUTHORIZED)
    
    elif request.method == 'DELETE':
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "댓글 작성자와 사용자가 다릅니다."}, status=status.HTTP_401_UNAUTHORIZED)


