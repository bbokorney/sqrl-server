from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^login/(?P<id>\w+)', views.login),
                       url(r'^login/', views.login),
                       )
