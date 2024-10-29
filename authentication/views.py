from django.shortcuts import render
from .serializers import UserLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response
from rest_framework import status

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User authenticated successfully
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)

            response_data = {
                "message": "User authenticated successfully",
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )



