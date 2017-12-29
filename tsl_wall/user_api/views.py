from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from importlib import import_module
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework import status
from django.core.mail import send_mail
import datetime


def init_session(session_key):
    """
    Initialize same session as done for ``SessionMiddleware``.
    """
    engine = import_module(settings.SESSION_ENGINE)
    return engine.SessionStore(session_key)


def get_all_logged_in_users_ids():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    return uid_list



####
# Work around with CORS preflight
# handle OPTIONS manually
####
@api_view(['GET', 'POST', 'OPTIONS'])
@csrf_exempt
def user_view(request):
    try:
        serializer_class = UserSerializer
        if request.method == "OPTIONS":
            response = HttpResponse()
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
            response['Access-Control-Max-Age'] = 1000
            # note that '*' is not valid for Access-Control-Allow-Headers
            response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
            return response

        if request.method == 'GET':
            queryset = User.objects.all()
            serialized_data = serializer_class(queryset, many=True).data
            response = Response(serialized_data, status=status.HTTP_200_OK)
            response['Access-Control-Allow-Origin'] = '*'
            return response

        if request.method == 'POST':
            serializer = serializer_class(data=request.POST)
            username = request.POST['username']
            email = request.POST['email']
            if serializer.is_valid():
                serializer.save()
                response = Response(serializer.data, status=status.HTTP_201_CREATED)
                response['Access-Control-Allow-Origin'] = '*'
                try:
                    send_mail(
                        'Hi ' + username + '! Welcome to MessageWall!',
                        'Thanks for using it enjoy!',
                        '313273828@qq.com',
                        [email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(str(e))
                return response
            else:
                response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                response['Access-Control-Allow-Origin'] = '*'
                return response
    except Exception as e:
        print(str(e))
        response = JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response['Access-Control-Allow-Origin'] = '*'
        return response


@csrf_exempt
def logout_view(request):
    if request.method == "OPTIONS":
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Max-Age'] = 1000
        # note that '*' is not valid for Access-Control-Allow-Headers
        response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
        return response
    if request.method == 'POST':
        found = False
        username = request.POST['username']
        user_id = request.POST['user_id']
        request = HttpRequest()
        now = datetime.datetime.now()
        sessions = Session.objects.filter(expire_date__gt=now)
        for session in sessions:
            cur_id = session.get_decoded().get('_auth_user_id')
            if cur_id == user_id:
                found = True
                request.session = init_session(session.session_key)
                logout(request)
        if found:
            response = JsonResponse({'status': 200}, status=status.HTTP_200_OK)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            response = JsonResponse({'status': 403}, status=status.HTTP_403_FORBIDDEN)
            response['Access-Control-Allow-Origin'] = '*'
            return response


@csrf_exempt
def login_view(request):

    if request.method == "OPTIONS":
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Max-Age'] = 1000
        # note that '*' is not valid for Access-Control-Allow-Headers
        response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
        return response
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_authenticated():
            login(request, user)
            response = JsonResponse({'status': 200, 'username': user.username, 'user_id': user.pk},
                                    status=status.HTTP_200_OK)
            response['Access-Control-Allow-Origin'] = '*'
            return response
        response = JsonResponse({'status': 403}, status=status.HTTP_403_FORBIDDEN)
        response['Access-Control-Allow-Origin'] = '*'
        return response
