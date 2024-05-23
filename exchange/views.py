from rest_framework.response import Response
from .models import Exchange
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .serializers import ExchangeSerializer
from constants import EXCHANGE_API_URL

def update_exchange_data(response):
    """
    API 응답을 받아와서 데이터베이스에 저장하고, 그 결과를 반환합니다.
    params:
    - response: API로부터 받아온 응답 데이터
    """
    Exchange.objects.all().delete()
    serializer = ExchangeSerializer(data=response, many=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data
    return None

@api_view(['GET'])
def index(request):
    """
    API를 호출하여 환율 데이터를 가져오고, 그 결과를 반환합니다.
    params:
    - request: 클라이언트로부터 받아온 HTTP 요청
    """
    response = requests.get(EXCHANGE_API_URL).json()
    if response:
        data = update_exchange_data(response)
        if data is not None:
            return Response(data, status=status.HTTP_200_OK)
    return Response({"detail": "Failed to update exchange data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)