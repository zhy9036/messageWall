from django.conf.urls import url
import user_api.views as views


urlpatterns = [

    url(r'^$', views.user_view, name='user_api'),
    url(r'^login/$', views.login_view, name='user_api_login'),
    url(r'^logout/$', views.logout_view, name='user_api_logout'),
    #url(r'^(?P<pk>\d+)/$', views.MessageDetailAPIView.as_view(), name='detail'),
]