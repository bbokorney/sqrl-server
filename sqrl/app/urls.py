from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^login/', views.login, name='login'),
                       url(r'^sqrl/(?P<token>[0-9a-f]{32}$)', views.sqrl, name='sqrl'),
                       )
