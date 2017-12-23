from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
import datetime
from django.http import HttpRequest
from django.core.urlresolvers import reverse
from importlib import import_module
from django.conf import settings
# Create your views here.
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from message_pool.forms import UserForm
from django.core.mail import send_mail

def main_view(request):
    user = None
    user_form = UserForm(data=request.POST)
    try:
        if request.user.is_authenticated():
            user = request.user
    except (AttributeError, KeyError):
        pass
    return render(request, 'message_pool/pool_base.html', {'user': user, 'form': user_form})



def get_all_logged_in_users_ids1():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    return uid_list


def init_session(session_key):
    """
    Initialize same session as done for ``SessionMiddleware``.
    """
    engine = import_module(settings.SESSION_ENGINE)
    return engine.SessionStore(session_key)


def get_all_logged_in_users_ids():
    now = datetime.datetime.now()
    uid_list = []
    sessions = Session.objects.filter(expire_date__gt=now)
    for session in sessions:
        user_id = session.get_decoded().get('_auth_user_id')
        uid_list.append(user_id)
    return uid_list


####
# Work around with CORS preflight
# cross site request
####
#@ensure_csrf_cookie
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
            response = JsonResponse({'status': 200, 'username': user.username, 'user_id': user.pk})
            response['Access-Control-Allow-Origin'] = '*'
            return response
        response = JsonResponse({'status': 401})
        response['Access-Control-Allow-Origin'] = '*'
        return response


@csrf_exempt
def register_view(request):

    if request.method == "OPTIONS":
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Max-Age'] = 1000
        # note that '*' is not valid for Access-Control-Allow-Headers
        response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
        return response

    if request.method == 'POST':
        '''
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            print(user.username, user_form.cleaned_data['password'])

            user = authenticate(username=user.username, password=user_form.cleaned_data['password'])
            if user.is_authenticated():
                login(request, user)
        else:
            return Http404
        '''
        print("***********************", request.POST)
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        userset = User.objects.filter(username=username)
        if userset.first() is None:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
            response = JsonResponse({'status': 200})
            response['Access-Control-Allow-Origin'] = '*'
            send_mail(
                'Hi ' + username + '! Welcome to MessageWall!',
                'Thanks for using it enjoy!',
                '313273828@qq.com',
                [email],
                fail_silently=False,
            )
            return response
        else:
            response = JsonResponse({'status': 401, 'error': 'Username not available'})
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
        username = request.POST['username']
        user_id = request.POST['user_id']
        request = HttpRequest()
        now = datetime.datetime.now()
        sessions = Session.objects.filter(expire_date__gt=now)
        for session in sessions:
            cur_id = session.get_decoded().get('_auth_user_id')
            if cur_id == user_id:
                request.session = init_session(session.session_key)
                logout(request)
        response = JsonResponse({'status': 200})
        response['Access-Control-Allow-Origin'] = '*'
        return response
