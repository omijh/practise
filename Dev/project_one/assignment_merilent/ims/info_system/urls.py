from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add', views.edit, name='add'),
    url(r'^(?P<id>\d+)/edit/$', views.edit, name="edit"),
    url(r'^(?P<id>\d+)/delete/$', views.delete, name="delete"),

]
