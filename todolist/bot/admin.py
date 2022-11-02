from django.contrib import admin

class BotAdmin(admin.ModelAdmin):
    list_display = ("tg_user_id", "tg_chat_id", "user")
    search_fields = ("tg_user_id", "tg_chat_id", "user")
