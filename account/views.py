from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from account.swagger.apidoc_definitions import REGISTER_VIEW_DEFINITION, LOGIN_REFRESH_DEFINITION, LOGIN_VIEW_DEFINITION

from .serializers import UserSerializer


class RegisterView(APIView):
    """
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @swagger_auto_schema(**REGISTER_VIEW_DEFINITION)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                **serializer.validated_data
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    throttle_scope = "token_obtain"

    @swagger_auto_schema(**LOGIN_VIEW_DEFINITION)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginRefreshView(TokenRefreshView):
    throttle_scope = "token_refresh"

    @swagger_auto_schema(**LOGIN_REFRESH_DEFINITION)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
        