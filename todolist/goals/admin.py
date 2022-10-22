from django.contrib import admin

from goals.models import Category, Goal, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "created", "updated")
    search_fields = ("title", "user", "category")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("goal", "user", "created", "updated")
    search_fields = ("goal", "user", "text")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
