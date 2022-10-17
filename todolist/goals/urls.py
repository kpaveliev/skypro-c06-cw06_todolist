from django.urls import path
import goals.views as views

urlpatterns = [
    path("goal_category/create", views.CategoryCreateView.as_view()),
]