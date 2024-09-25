from django.urls import path
from .views import ThreadCreateView

urlpatterns = [
    path('v1/threads/', ThreadCreateView.as_view(), name='thread-create')
]