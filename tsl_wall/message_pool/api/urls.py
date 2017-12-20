from django.conf.urls import url
from django.contrib import admin
import message_pool.api.views as views

urlpatterns = [

    url(r'^$', views.MessageListAPIView.as_view(), name='list'),
]