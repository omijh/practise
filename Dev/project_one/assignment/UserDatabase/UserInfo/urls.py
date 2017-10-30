from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addedit', views.addedit, name='addedit'),
    url(r'^(?P<id>\d+)/edit/$', views.edit, name="update"),
    # url(r'^update/(?P<id>\d+)$', views.update),
    url(r'(?P<slug>[-\w]+)/edit/$', views.edit, name="edit"),
]