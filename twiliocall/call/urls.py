from . import views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.redirect),
    url(r'^call/$', views.call_request, name ='call_request'),
    url(r'^call/call_made$', views.make_call, name='call_made')
    ]