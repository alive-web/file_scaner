from django.conf.urls import patterns, url
from cga.management_scanner import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

)