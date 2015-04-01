from django.conf.urls import patterns, url
from cga.management_scanner import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^get_files/$', views.get_files, name='get_files'),
    url(r'^api_logs/$', views.api_logs, name='api_logs'),
)