from django.conf.urls import url
import message_pool.api.views as views

urlpatterns = [

    url(r'^$', views.message_view, name='message_api'),
    #url(r'^(?P<pk>\d+)/$', views.MessageDetailAPIView.as_view(), name='detail'),
]