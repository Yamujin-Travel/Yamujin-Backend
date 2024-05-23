from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),  # Django 관리자 사이트
    path('users/', include('accounts.urls')),  # 사용자 관련 기능 (프로필 보기, 수정 등)
    path('board/', include('articles.urls')),  # 게시판 관련 기능 (게시글 작성, 조회 등)
    path('exchange/', include('exchange.urls')),  # 환전 관련 기능
    path('financial/', include('financial.urls')),  # 금융 관련 기능
    path('accounts/', include('dj_rest_auth.urls')),  # 계정 관련 기능 (로그인, 로그아웃 등)
    path('accounts/registration/', include('dj_rest_auth.registration.urls')),  # 계정 등록 관련 기능 (회원가입 등)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # API 스키마
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
