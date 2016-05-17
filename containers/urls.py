from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.containers_list, name='containers_list'),
]
