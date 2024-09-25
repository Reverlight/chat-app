from django.shortcuts import get_object_or_404
from rest_framework import generics

from chat.models import Thread
from chat.serializers import ThreadSerializer


class ThreadCreateView(generics.CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def perform_create(self, serializer):
        if get_object_or_404(self.queryset, participants__in=serializer.data['participants']):
            # Thread already exists, we avoid creating it again
            pass
        else:
            serializer.save()
