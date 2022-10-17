from django.urls import path
import goals.views as views

urlpatterns = [
    path("goal_category/create", views.CategoryCreateView.as_view()),
    path("goal_category/list", views.CategoryListView.as_view()),
    path("goal_category/<pk>", views.CategoryView.as_view()),
]