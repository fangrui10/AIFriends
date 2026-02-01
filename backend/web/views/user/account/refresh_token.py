# 用refresh_token刷新获取新的access_token

import re
from weakref import ref
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response({
                    "result": "refresh token不存在"
                },
                status=401) # 自己定义状态码401表示未授权
            refresh = RefreshToken(refresh_token)
            if settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"]: # 刷新access时会同时刷新refresh token
                refresh.set_jti()
                response = Response({
                    "result": "success",
                    "access": str(refresh.access_token),
                })
                response.set_cookie(
                    key = "refresh_token",
                    value = str(refresh),
                    httponly = True,
                    samesite = 'Lax',
                    secure = True,
                    max_age = 7 * 24 * 60 * 60, # 七天
                )
                return response
            return Response({
                "result": "success",
                "access": str(refresh.access_token),
            })
        
        except:
            return Response({
                "result": "refresh token无效或已过期"
                },
                status=401) # 自己定义状态码401表示未授权
