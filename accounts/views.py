from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, username):
    """
    사용자 프로필을 조회하는 API입니다.
    params:
    - username: 조회하려는 사용자의 username
    """
    if request.user.username == username:
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_info(request, username):
    """
    사용자 정보를 조회하거나 수정하는 API입니다.
    params:
    - username: 조회하거나 수정하려는 사용자의 username
    """
    if request.user.username == username:
        user = get_object_or_404(get_user_model(), username=username)
        if request.method == 'GET':
            serializer = UserInfoSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            serializer = UserInfoSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# TODO: 사용자가 기본 프로필 이미지 중 하나를 선택할 수 있도록 기능 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_info_profile(request, username):
    """
    사용자 프로필 이미지를 수정하는 API입니다.
    params:
    - username: 프로필 이미지를 수정하려는 사용자의 username
    """
    if request.user.username == username:
        user = get_object_or_404(get_user_model(), username=username)
        data = { 'profile_img': request.data['profile_img[]']}
        serializer = UserInfoSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

