from django.contrib import admin

from goals.models import Category, Goal


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "created", "updated")
    search_fields = ("title", "user", "category")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goal, CategoryAdmin)
