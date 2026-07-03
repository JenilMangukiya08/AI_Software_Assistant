from django.db import models
from django.contrib.auth.models import User


class Repository(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="repositories"
    )

    name = models.CharField(max_length=200)

    github_url = models.URLField()

    collection_name = models.CharField(max_length=200)

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "github_url"],
                name="unique_repository_per_user"
            )
        ]

    def __str__(self):
        return self.name


class ChatSession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chat_sessions"
    )

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title if self.title else f"Session {self.id}"


class ChatMessage(models.Model):

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.CharField(max_length=10)

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.sender