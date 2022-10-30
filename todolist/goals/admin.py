from django.contrib import admin

from goals.models import Category, Goal, Comment, Board


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")
    readonly_fields = ("created", "updated")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "created", "updated")
    search_fields = ("title", "user", "category")
    readonly_fields = ("created", "updated")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("goal", "user", "created", "updated")
    search_fields = ("goal", "user", "text")
    readonly_fields = ("created", "updated")


class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "updated")
    search_fields = ("title",)
    readonly_fields = ("created", "updated")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Board, BoardAdmin)
