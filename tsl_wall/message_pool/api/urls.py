from django.conf.urls import url
from django.contrib import admin
import message_pool.api.views as views

urlpatterns = [

    url(r'^$', views.message_view, name='list'),
    #url(r'^(?P<pk>\d+)/$', views.MessageDetailAPIView.as_view(), name='detail'),
]