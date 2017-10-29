from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addedit', views.addedit, name='addedit'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name="edit"),
    # url(r'^update/(?P<id>\d+)$', views.update),
    url(r'(?P<slug>[-\w]+)/edit/$', views.edit, name="edit"),
]