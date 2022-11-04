from django.urls import path
import tg.views as views

urlpatterns = [
    path("verify", views.TgUserUpdateView.as_view()),
]