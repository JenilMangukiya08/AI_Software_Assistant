from django.contrib import admin

# Register your models here.
from .models import (
    Repository,
    ChatSession,
    ChatMessage
)

admin.site.register(Repository)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)