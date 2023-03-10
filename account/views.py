from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema

from account.swagger import apidocs
from account.serializers import UserSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @swagger_auto_schema(**apidocs.REGISTER_VIEW)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                **serializer.validated_data
            )
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)

@method_decorator(name='post',
    decorator=swagger_auto_schema(**apidocs.LOGIN_VIEW))
class LoginView(TokenObtainPairView):
    throttle_scope = "token_obtain"


@method_decorator(name='post',
    decorator=swagger_auto_schema(**apidocs.LOGIN_REFRESH_VIEW))
class LoginRefreshView(TokenRefreshView):
    throttle_scope = "token_refresh"
        