from django.conf.urls import url
from . import views
from .views import payment_request,drop_down_list,save_payment_form,export_payment_request,export_payment_form,export_csv,upload_ack

urlpatterns = [
	url(r'^payment_request/$', payment_request, name = 'payment_request'),
	url(r'^export_payment_request/$', export_payment_request, name = 'export_payment_request'),
	url(r'^ajax_load_branch/$', drop_down_list, name='ajax_load_branch'),
	url(r'^save_payment_form/$', save_payment_form, name='save_payment_form'), 
	url(r'^export_payment_form/$', export_payment_form, name='export_payment_form'),
	url(r'^export_payment_form/(?P<datefrom>\d{4}-\d{2}-\d{2})/(?P<dateto>\d{4}-\d{2}-\d{2})$', export_csv, name='export_csv'),
    url(r'^payment_request/(?P<des>[a-z]{1})/(?P<id>\d+)/approve/$', views.approve, name="approve"),
    url(r'^payment_request/(?P<des>[a-z]{1})/(?P<id>\d+)/decline/$', views.decline, name="decline"),
	url(r'^upload_ack/$', upload_ack, name='upload_ack'),

]