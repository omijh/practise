# url file for userapp

from django.conf.urls import url
from django.contrib import admin
from .custom_decorators import *
from .views import * 

urlpatterns = [

# url to add a new employee
url(r'^add_employee/$', add_employee, name = 'add_employee'),

# url to save emplyee details in database
url(r'^save_employee/$', save_employee, name = 'save_employee'),

# ajax url to show dependent dropdown mapping for location
url(r'^ajax/load-cities/$', drop_down_list, name='ajax_load_cities'), 

# to get employee details whose emp_code is selected from list view
# ex: /00001/
url(r'^employee_detail/(?P<emp_code>[0-9]+)/$',employee_detail, name = 'employee_detail'),

# to show employee details to branch manager for approval
# ex: employee_approval/10001/
url(r'^employee_approval/(?P<emp_code>[0-9]+)/$',employee_approval, name = 'employee_approval'),

# to send approve employee email to helpdesk
url(r'^approve_employee/$', approve_employee, name = 'approve_employee'),

# to send reject employee email to helpdesk 
url(r'^reject_employee/$', reject_employee, name = 'reject_employee'),

# url to list all employee records
url(r'^$', index, name = 'index'),

# url to View Apps Details in Database
url(r'^app_account_list/$', app_account_list, name = 'app_account_list'),

# url to View Apps Details in Database
url(r'^app_account_form/(?P<emp_code>[0-9]+)/$', app_account_form, name = 'app_account_form'),

# url to edit employee app username
url(r'^edit_emp_app/(?P<emp_app_detail_id>[0-9]+)/$', edit_emp_app, name = 'edit_emp_app'),

# url to show employee detail and app access detail to app admin
url(r'^emp_app_detail/(?P<emp_app_detail>[0-9]+)/$', emp_app_detail, name = 'emp_app_detail'),

# ajax url to validate emp_code
url(r'^ajax/validate_emp_code/$', validate_emp_code, name='validate_emp_code'),

# ajax url to validate emp_id
url(r'^ajax/validate_email_id/$', validate_email_id, name='validate_email_id'),

# ajax url to select country ext
url(r'^ajax/select_country_ext/$', select_country_ext, name='select_country_ext'),

# form to show nav application details to Service Now
url(r'^nav_app_detail/(?P<emp_app_detail>[0-9]+)/$', nav_app_detail, name = 'nav_app_detail'),

# save app access approval 
url(r'^save_nav_access_approval/$', save_nav_access_approval, name = 'save_nav_access_approval'),

url(r'^nav_access_approval/(?P<emp_code>[0-9]+)/(?P<app_id>[0-9]+)/$', nav_access_approval, name = 'nav_access_approval'),

url(r'^emp_log_list/(?P<emp_code>[0-9]+)/$', emp_log_list, name = 'emp_log_list'),

# DSP app access 
url(r'^dsp_app_detail/(?P<emp_app_detail>[0-9]+)/$', dsp_app_detail, name = 'dsp_app_detail'),

# DSP app access 
url(r'^save_dsp_access_detail/(?P<emp_app_detail>[0-9]+)/$', save_dsp_access_detail, name = 'save_dsp_access_detail'),

# SPA app access 
url(r'^spa_app_detail/(?P<emp_app_detail>[0-9]+)/$', spa_app_detail, name = 'spa_app_detail'),

# SPA app access 
url(r'^save_spa_access_detail/(?P<emp_app_detail>[0-9]+)/$', save_spa_access_detail, name = 'save_spa_access_detail'),

url(r'^app_info_holder/(?P<emp_app_detail>[0-9]+)/$', app_info_holder, name = 'app_info_holder'),

url(r'^reject_app_info/(?P<emp_app_detail>[0-9]+)/$', reject_app_info, name = 'reject_app_info'),

url(r'^approve_app_info/(?P<emp_app_detail>[0-9]+)/$', approve_app_info, name = 'approve_app_info'),

url(r'^stp_app_form/(?P<emp_app_detail>[0-9]+)/$', stp_app_view, name='stp_app_view'),

url(r'^stp_app_save/(?P<emp_app_detail>[0-9]+)/$', stp_app_save, name='stp_app_save'),

url(r'^app_stp_detail/(?P<emp_app_detail>[0-9]+)/$', stp_app_2, name='stp_app_2'),

# url to Edit employee details
url(r'^edit_employee/(?P<emp_code>[0-9]+)/$', edit_employee, name = 'edit_employee'),

# url to save edit employee details in temp employee table
url(r'^temp_edit_employee/(?P<emp_code>[0-9]+)/$', temp_edit_employee, name = 'temp_edit_employee'),

# url to show edit approval form to Reporting Authority
url(r'^edit_employee_approval/(?P<emp_code>[0-9]+)/$', edit_employee_approval, name = 'edit_employee_approval'),

# to send approve edit employee email to helpdesk
url(r'^approve_employee_edit/$', approve_employee_edit, name = 'approve_employee_edit'),

# to send reject edit employee email to helpdesk 
url(r'^reject_employee_edit/$', reject_employee_edit, name = 'reject_employee_edit'),

# to send employee activate/deactivate approval mail to HR
url(r'^active_deactive_employee/(?P<emp_code>[0-9]+)/(?P<action_taken>[a-z]+)/$', active_deactive_employee, name = 'active_deactive_employee'),

# to show employee activate/deactivate approval form to HR
url(r'^active_deactive_employee_approval/(?P<emp_code>[0-9]+)/(?P<action_taken>[a-z]+)/$', active_deactive_employee_approval, name = 'active_deactive_employee_approval'),

# to deactive employee
url(r'^approve_active_deactive_employee/(?P<action_taken>[a-z]+)/$', approve_active_deactive_employee, name = 'approve_active_deactive_employee'),

# to activate employee 
url(r'^reject_active_deactive_employee/(?P<action_taken>[a-z]+)/$', reject_active_deactive_employee, name = 'reject_active_deactive_employee'),

]

