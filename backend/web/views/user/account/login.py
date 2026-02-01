# 使用用户名密码登录，在cookies中设置refresh_token，并返回access_token给前端
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from web.models.user import UserProfile


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get("user").strip()
            password = request.data.get("password").strip()
            if not username or not password:
                return Response({
                    "result": "用户名和密码不能为空"
                })
            user = authenticate(username=username, password=password)
            if user: # 如果不为空则用户名密码正确
                user_profile = UserProfile.objects.get(user=user) # 取出用户信息
                refresh = RefreshToken.for_user(user) # 生成jwt
                response = Response({
                    "result": "success",
                    "access": str(refresh.access_token),
                    "user_id": user.id,
                    "username": user.username,
                    "photo": user_profile.photo.url,
                    "profile": user_profile.profile,
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
                "result": "用户名或密码错误"
            })


        except:
            return Response({
                "result": "系统异常，请稍后重试"
            })