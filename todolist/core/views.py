from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import SignUpSerializer, RetrieveUpdateSerializer


class SignUpView(CreateAPIView):
    """Create new user"""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class LoginView(APIView):
    """Login user"""

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


# @ensure_csrf_cookie
class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = RetrieveUpdateSerializer
