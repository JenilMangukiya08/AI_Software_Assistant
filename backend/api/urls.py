from django.urls import path
from .views import (
    RepositoryUploadView,
    ChatAPIView,
    RepositoryTreeView,
    SymbolSearchView,
    RegisterView,
    ChatHistoryAPIView,
    ChatMessagesAPIView,
    DeleteChatAPIView,
    RenameChatAPIView,
    ProfileAPIView,
    RepositoryListAPIView,
    RepositoryStatsAPIView,
    DeleteRepositoryAPIView
    )

urlpatterns = [
    path(
        "upload-repository/",
        RepositoryUploadView.as_view(),
        name="upload_repository"
    ),
    path(
        "chat/",
        ChatAPIView.as_view(),
        name="chat"
    ),
    path(
        "repository-tree/",
        RepositoryTreeView.as_view(),
    ),
    path(
        "symbol-search/",
        SymbolSearchView.as_view()
    ),

    path(
        "register/",
        RegisterView.as_view()
    ),

    path(
        "history/",
        ChatHistoryAPIView.as_view()
    ),

    path(
        "history/<int:session_id>/",
        ChatMessagesAPIView.as_view()
    ),

    path(
        "history/delete/<int:session_id>/",
        DeleteChatAPIView.as_view()
    ),

    path(
        "history/rename/<int:session_id>/",
        RenameChatAPIView.as_view()
    ),

    path(
        "profile/",
        ProfileAPIView.as_view()
    ),

    path(
        "repositories/",
        RepositoryListAPIView.as_view()
    ),

    path(
        "repositories/<int:repository_id>/stats/",
        RepositoryStatsAPIView.as_view()
    ),

    path(
        "repositories/<int:repository_id>/delete/",
        DeleteRepositoryAPIView.as_view()
    ),
]