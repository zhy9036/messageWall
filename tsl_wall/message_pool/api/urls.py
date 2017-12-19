from django.conf.urls import url
from django.contrib import admin

from .views import MessageListAPIView

urlpatterns = [

    url(r'^$', MessageListAPIView.as_view(), name='list'),
]