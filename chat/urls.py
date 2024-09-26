from django.urls import path

from .views import (
    MessageCreateView,
    MessageListView,
    MessageUpdateView,
    ThreadCreateView,
    ThreadDestroyView,
    ThreadListView,
    ThreadMessageListView
)


urlpatterns = [
    # Threads
    path('v1/threads/', ThreadCreateView.as_view(), name='threads-create'),
    path('v1/threads/<int:pk>', ThreadDestroyView.as_view(), name='threads-destroy'),
    path(
        'v1/threads/<int:thread_id>/messages',
        ThreadMessageListView.as_view(),
        name='thread-messages-get'
         ),
    # Messages
    path('v1/messages/<int:pk>', MessageUpdateView.as_view(), name='messages-update'),
    path('v1/messages/', MessageCreateView.as_view(), name='messages-create'),
    # Users
    path('v1/users/<int:user_id>/threads', ThreadListView.as_view(), name='users-threads-list'),
    path('v1/users/<int:user_id>/messages', MessageListView.as_view(), name='users-unread-messages-list'),
]