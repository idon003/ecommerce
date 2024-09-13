from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer
from ..models import CustomUser

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Authentication"])
class RegisterView(APIView):
    serializer_class = CustomUserSerializer
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token_data = TokenObtainPairSerializer.get_token(user)
            tokens = {
                "access": str(token_data.access_token),
                "refresh": str(token_data),
            }

            return Response({"user": serializer.data, "tokens": tokens}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Authentication"])
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

@extend_schema(tags=["Authentication"])
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
