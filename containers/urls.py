from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.containers_list, name='containers_list'),
    url(r'^container/(?P<pk>[0-9]+)/$', views.container_details, name='container_details'),
]
