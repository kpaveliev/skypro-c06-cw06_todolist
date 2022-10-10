from django.urls import path
from .views import SignUpView, LoginView, UserRetrieveUpdateView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>/', UserRetrieveUpdateView.as_view())
]
