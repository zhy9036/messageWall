from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


# Create your views here.
def main_view(request):
    user = None
    try:
        if request.user.is_authenticated():
            user = request.user
    except (AttributeError, KeyError):
        pass
    return render(request, 'message_pool/pool_base.html', {'user': user})


def login_view(request):
    username = request.POST['uname']
    password = request.POST['psw']
    user = authenticate(username=username, password=password)
    if user.is_authenticated():
        login(request, user)
    return HttpResponseRedirect('/pool/')



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pool/')