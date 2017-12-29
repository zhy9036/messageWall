
from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'^$', views.message_view, name='message_api'),

]