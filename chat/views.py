from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from chat.models import Thread, Message
from chat.permissions import IsThreadParticipant, IsAllowedMarkMessageRead
from chat.serializers import ThreadSerializer, MessageSerializer, MessageUpdateSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ThreadCreateView(generics.CreateAPIView):
    """
    Creates thread with participants (limited to 2)
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.queryset.filter(participants__in=serializer.validated_data['participants']).distinct():
            # Thread already exists, we avoid creating it again
            pass
        else:
            serializer.save()


class ThreadMessageListView(generics.ListAPIView):
    """
    Retrieves messages for a specific thread
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsThreadParticipant]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        return Message.objects.filter(thread_id=thread_id)


class MessageListView(generics.ListAPIView):
    """
    Retrieves all unread messages for a user
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # User get unread messages for other participants, so we exclude sender user_id
        user_id = self.kwargs['user_id']
        if user_id != self.request.user.id:
            raise PermissionDenied('You cannot read messages of other users')
        return Message.objects.filter(
            thread__participants__in=[user_id],
            is_read=False
        ).exclude(sender=user_id)


class ThreadListView(generics.ListAPIView):
    """
    Retrieves all threads for a user
    """
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        if not get_object_or_404(User, pk=user_id):
            raise NotFound(f'User {user_id} does not exist')
        return Thread.objects.filter(participants__in=[user_id])


class ThreadDestroyView(generics.DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated, IsThreadParticipant]


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.id != serializer.validated_data['sender'].id:
            raise PermissionDenied(detail='You are not the actual sender!')

        if not get_object_or_404(
            Thread,
            participants__in=[
                serializer.validated_data['sender']
            ],
            id=serializer.validated_data['thread'].id,
        ):
            raise PermissionDenied(detail='You are not the part of the thread')

        serializer.save()


class MessageUpdateView(generics.UpdateAPIView):
    """
        Updates message to be read
    """
    serializer_class = MessageUpdateSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMarkMessageRead]
