# 注册账号。创建账号后返回refresh_token、access_token和用户信息给前端

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User  # 导入User数据库
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile



class RegisterView(APIView):
    def post(self, request):
        try:
            username = request.data["username"].strip()
            password = request.data["password"].strip()
            if not username or not password:
                return Response({"result": "用户名和密码不能为空"})
            if User.objects.filter(username=username).exists():
                return Response({"result": "用户名已存在"})
            user = User.objects.create_user(username=username, password=password)
            user_profile = UserProfile.objects.create(user=user)
            refresh = RefreshToken.for_user(user)  # 生成jwt
            response = Response(
                {
                    "result": "success",
                    "access": str(refresh.access_token),
                    "user_id": user.id,
                    "username": user.username,
                    "photo": user_profile.photo.url,
                    "profile": user_profile.profile,
                }
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                samesite="Lax",
                secure=True,
                max_age=7 * 24 * 60 * 60, # 七天
            )
            return response  
        except:
            return Response({"result": "系统异常，请稍后重试"})
