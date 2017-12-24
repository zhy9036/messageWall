from django.conf.urls import url
import user_api.views as views


urlpatterns = [

    url(r'^$', views.user_view, name='user_api'),
    #url(r'^(?P<pk>\d+)/$', views.MessageDetailAPIView.as_view(), name='detail'),
]