from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from message_pool.forms import UserForm


def main_view(request):
    user = None
    user_form = UserForm(data=request.POST)
    try:
        if request.user.is_authenticated():
            user = request.user
    except (AttributeError, KeyError):
        pass
    return render(request, 'message_pool/pool_base.html', {'user': user, 'form': user_form})


@csrf_exempt
def login_view(request):
    ####
    # Work around with CORS preflight
    # cross site request
    ####
    if request.method == "OPTIONS":
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Max-Age'] = 1000
        # note that '*' is not valid for Access-Control-Allow-Headers
        response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
        return response
    if request.method == "POST":
        print("******************************", request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_authenticated():
            login(request, user)
            response = JsonResponse({'status': 200})
            response['Access-Control-Allow-Origin'] = '*'
            return response
        response = JsonResponse({'status': 401})
        response['Access-Control-Allow-Origin'] = '*'
        return response


def register_view(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            print(user.username, user_form.cleaned_data['password'])

            user = authenticate(username=user.username, password=user_form.cleaned_data['password'])
            if user.is_authenticated():
                login(request, user)
        else:
            return Http404
    return HttpResponseRedirect('/pool/')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pool/')