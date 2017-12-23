from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from message_pool.views import get_all_logged_in_users_ids

from rest_framework.response import Response

from message_pool.models import Message
from message_pool.api.serializers import MessageDetailSerializer, MessageListSerializer
'''
# Create your views here.


class MessageDetailAPIView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer


class MessageListAPIView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer
'''


@csrf_exempt
@api_view(['GET', 'POST', 'OPTIONS'])
def message_view(request):
    serializer_class = MessageListSerializer

    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Max-Age'] = 1000
        # note that '*' is not valid for Access-Control-Allow-Headers
        response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
        return response

    if request.method == 'GET':
        queryset = Message.objects.all()
        serialized_data = serializer_class(queryset, many=True).data
        response = Response(serialized_data, status=status.HTTP_200_OK)
        response['Access-Control-Allow-Origin'] = '*'
        return response

    if request.method == 'POST':
        ids = get_all_logged_in_users_ids()
        user_id = request.POST['user_id']
        if user_id not in ids:
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        serializer = serializer_class(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            response['Access-Control-Allow-Origin'] = '*'
            return response

