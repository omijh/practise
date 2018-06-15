from django.conf.urls import url
from django.contrib import admin
from .views import leave_application,add_leave_type,submit_leave_type,leave_application_list,export_to_excel,import_holiday_list_excel,submit_leave,add_holiday,add_holiday_type,submit_holiday_type,submit_new_holiday,holiday_list_search_view,list_holiday_index,leave_index,leave_approval,approved_leave,reject_leave,view_balanced_leave,add_balanced_leave,import_emp_balanced_leave_list_excel,validate_send,emp_code_validate, edit_leave_application, leave_logs_list,cancel_leave_application, error_go_back

# url file for userapp

urlpatterns = [

# url to Apply For Leave 
url(r'^leave_application/$', leave_application, name = 'leave_application'),

# url to Apply For Leave 
url(r'^leave_application_list/$', leave_application_list, name = 'leave_application_list'),

# url to get Leave Detail 
url(r'^edit_leave_application/(?P<leave_id>[0-9]+)/$', edit_leave_application, name = 'edit_leave_application'),

# Url to Cancel Leave Application
url(r'^cancel_leave_application/(?P<emp_code>[0-9]+)/(?P<leave_id>[0-9]+)/$', cancel_leave_application, name = 'cancel_leave_application'),

# Url to Maintain Logs of Leave Application  
url(r'^leave_logs_list/(?P<leave_id>[0-9]+)/$', leave_logs_list, name = 'leave_logs_list'),


# Url to Validate Errors 
url(r'^error_go_back/$', error_go_back, name = 'error_go_back'),

# Url to Add Leave Type 
url(r'^add_leave_type/$', add_leave_type, name = 'add_leave_type'),

# url to Submit Leave Application
url(r'^submit_leave/$', submit_leave, name = 'submit_leave'),

# Url to Submit Leave Type eg: Fixed Planned Leave,Casual Leave,Oustation Travelling,etc.
url(r'^submit_leave_type/$', submit_leave_type, name = 'submit_leave_type'),

# Url to View Balance Leave Report of User eg: Balanced PL-2,CL-1,etc.
url(r'^view_balanced_leave/$', view_balanced_leave, name = 'view_balanced_leave'),

# Url to ADD Balance Leave  of User eg: Balanced PL-2,CL-1,etc.
url(r'^add_balanced_leave/$', add_balanced_leave, name = 'add_balanced_leave'),

# Url to Add Holiday Date for Selected State
url(r'^add_holiday/$', add_holiday, name = 'add_holiday'),

# Url to Add Holiday Type 
url(r'^add_holiday_type/$', add_holiday_type, name = 'add_holiday_type'),

# Url to Submit Holiday Type eg: Fixed Holiday,Optional Holiday 
url(r'^submit_holiday_type/$', submit_holiday_type, name = 'submit_holiday_type'),

# Url to add Holidays Date for Selected State in Database
url(r'^submit_new_holiday/$', submit_new_holiday, name = 'submit_new_holiday'),

# Url to Direct to List/View Holidays where User can get holiday list by selecting state
url(r'^holiday_list_search_view/$', holiday_list_search_view, name = 'holiday_list_search_view'),

# Url to List/View Holidays Data for Selected State
url(r'^list_holiday_index/$', list_holiday_index, name = 'list_holiday_index'),

# Url to Export Excel File
url(r'^export_to_excel/$', export_to_excel, name = 'export_to_excel'),
# url(r'^export_to_csv/(?P<leave_branch>[a-z A-Z]+)/(?P<date_from>[a-z A-Z]+)/(?P<date_to>[a-z A-Z]+)/$', export_to_csv, name = 'export_to_csv'),


# to show Employee Detail who requested for Leaves to Branch Manager or Head Of Department for approval
# the link will get generated as ---(url)/(the employee code) 
# ex: leave_approval/10001/
url(r'^leave_approval/(?P<emp_code>[0-9]+)/(?P<leave_id>[0-9]+)$', leave_approval, name = 'leave_approval'),

# URL To Get Employee Details when user enter Emp Code in Leave Application Form
# url(r'^get_emp_details/$(?P<emp_code>[0-9]+)', get_emp_details, name = 'get_emp_details'),


# Url to Send mail to Employee after manager approves its Leave Request
url(r'^approved_leave/(?P<emp_code>[0-9]+)/(?P<leave_id>[0-9]+)$', approved_leave, name = 'approved_leave'),

# # Url to Send mail to Employee after manager approves its Leave Request
# url(r'^approved_leave/$', approved_leave, name = 'approved_leave'),


# Url to Send mail to Employee after manager Rejects its Leave Request
url(r'^reject_leave/(?P<leave_id>[0-9]+)/(?P<leave_emp_code>[0-9]+)$', reject_leave, name = 'reject_leave'),

# url to list all employee records
url(r'^leave_index$', leave_index, name = 'leave_index'),


# Url to Import Holiday List to Database
url(r'^import_holiday_list_excel$', import_holiday_list_excel, name = 'import_holiday_list_excel'),


# Url to Import Employee's Balanced Leave List to Database
url(r'^import_emp_balanced_leave_list_excel$', import_emp_balanced_leave_list_excel, name = 'import_emp_balanced_leave_list_excel'),

# ajax url to validate send
url(r'^ajax/validate_send/$', validate_send, name='validate_send'),

# ajax url to validate Emp Code
url(r'^ajax/emp_code_validate/$', emp_code_validate, name='emp_code_validate'),

]