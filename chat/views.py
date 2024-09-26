from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated

from chat.models import Thread, Message
from chat.permissions import IsThreadParticipant, IsAllowedMarkMessageRead
from chat.serializers import ThreadSerializer, MessageSerializer, MessageUpdateSerializer


class ThreadCreateView(generics.CreateAPIView):
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
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsThreadParticipant]

    def get_queryset(self):
        # Retrieve messages for a specific thread
        thread_id = self.kwargs['thread_id']
        return Message.objects.filter(thread_id=thread_id)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve unread messages for a user
        user_id = self.kwargs['user_id']
        return Message.objects.filter(
            thread__participants__in=[user_id],
            is_read=False
        ).exclude(sender=user_id)


class ThreadListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve messages for a specific thread
        user_id = self.kwargs['user_id']
        if not get_object_or_404(User, user_id=user_id):
            raise NotFound(f'User {user_id} does not exist')
        return Message.objects.filter(user_id=user_id)


class ThreadDestroyView(generics.DestroyAPIView):
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
    serializer_class = MessageUpdateSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, IsAllowedMarkMessageRead]
