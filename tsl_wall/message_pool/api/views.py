from django.shortcuts import render
from rest_framework.generics import ListAPIView
from message_pool.models import Message
# Create your views here.

class MessageListAPIView(ListAPIView):
    queryset = Message.objects.all()