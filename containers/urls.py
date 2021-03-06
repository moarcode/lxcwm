from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.containers_list, name='containers_list'),
#    url(r'^container/action/(?P<pk>[0-9]+)/$', views.container_start, name='container_start'),
    url(r'^container/(?P<pk>[0-9]+)/$', views.container_details, name='container_details'),
    url(r'^container/new/$', views.container_new, name='container_new'),
    url(r'^container/(?P<pk>[0-9]+)/edit/$', views.container_edit, name='container_edit'),
    url(r'^container/(?P<pk>[0-9]+)/start/$', views.container_start, name='container_start'),
    url(r'^container/(?P<pk>[0-9]+)/stop/$', views.container_stop, name='container_stop'),
    url(r'^container/(?P<pk>[0-9]+)/delete/$', views.container_delete, name='container_delete'),
]

