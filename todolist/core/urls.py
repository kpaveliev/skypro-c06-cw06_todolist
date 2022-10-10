from django.urls import path, include
from rest_framework import routers
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserCreateView

# users_router = routers.SimpleRouter()
# users_router.register('signup', UserViewSet)

urlpatterns = [
    # path('', include(users_router.urls)),
    path('signup/', UserCreateView.as_view())
    # path('token/', TokenObtainPairView.as_view()),
    # path('refresh/', TokenRefreshView.as_view()),
]
