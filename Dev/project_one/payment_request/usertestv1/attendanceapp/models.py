from django.db import models
from django import forms
from userapp.models import EmployeeMaster,BranchMaster,DivisionMaster,DesignationMaster,AppMaster,EmpAppDetail,AppRole,AppAdmin
IMPORT_FILE_TYPES = ['.xls', ]

# Create your models here.

# List of Branch Manager names & email
class LeaveTypesMaster(models.Model):
	leave_type = models.CharField(max_length=45, null=True)
	short_name_leave_type = models.CharField(max_length=45, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# List of Holidays according to State Selected
class HolidayListMaster(models.Model):
	holiday_name = models.CharField(max_length=45, null=True)
	holiday_date = models.DateTimeField(auto_now_add=True, null=True)
	holiday_day  = models.CharField(max_length=45)
	# fixed_holiday_date = models.DateTimeField(auto_now_add=True, null=True)
	# optional_holiday_date = models.DateTimeField(auto_now_add=True, null=True)
	
	holiday_type_id = models.ForeignKey('HolidayTypeMaster', models.DO_NOTHING, null=True)
	state_id = models.ForeignKey('StateName', models.DO_NOTHING, null=True)
	coverage = models.CharField(max_length=1000, null=True)
	# coverage = models.CharField(max_length=45, null=True)
	region = models.CharField(max_length=100, null=True)
	assigned_by = models.CharField(max_length=45, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


# Type of Holidays
class HolidayTypeMaster(models.Model):
	holiday_type = models.CharField(max_length=45, null=True)
	short_name_holiday_type = models.CharField(max_length=45, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# Type of Coverage
class CoverageMaster(models.Model):
	coverage = models.CharField(max_length=45, null=True)
	state_id = models.ForeignKey('StateName', models.DO_NOTHING, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# region_id = models.ForeignKey('RegionMaster', models.DO_NOTHING, null=True)


# Type of Region
class RegionMaster(models.Model):
	region = models.CharField(max_length=45, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# List of All States
class StateName(models.Model):
	state_name = models.CharField(max_length=45, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# coverage_id = models.ForeignKey('CoverageMaster', models.DO_NOTHING, null=True)
	# region_id = models.ForeignKey('RegionMaster', models.DO_NOTHING, null=True)

# List of Branch Manager names & email
class LeaveMaster(models.Model):
	emp_id = models.ForeignKey('userapp.EmployeeMaster', models.DO_NOTHING, null=True)
	emp_name = models.CharField(max_length=45, null=True)
	emp_code = models.CharField(max_length=45, null=True)
	emp_email = models.CharField(max_length=45, null=True)
	leave_status = models.CharField(max_length=45, null=True)
	leave_type_id = models.ForeignKey('LeaveTypesMaster', models.DO_NOTHING, null=True)
	holiday_type_id = models.ForeignKey('HolidayTypeMaster', models.DO_NOTHING, null=True)
	date_from = models.DateTimeField(null=True)
	date_to = models.DateTimeField(null=True)
	sick_lev_doc_pic = models.FileField(upload_to='media/doc', null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# document = models.FileField(upload_to='documents/',default = 'doc/logo.png')

# List of Branch Manager names & email
class BalancedLeaveMaster(models.Model):
	emp_code = models.CharField(max_length=45, null=True)
	emp_name = models.CharField(max_length=45, null=True)
	balanced_leave_type_id = models.ForeignKey('LeaveTypesMaster', models.DO_NOTHING, null=True)
	balanced_leave = models.CharField(max_length=45, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# To Import Excel Sheet into HolidayListMaster
# class UploadFileForm(forms.Form):
# 	file = forms.FileField()


# def upload(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             filehandle = request.FILES['file']
#             return excel.make_response(filehandle.get_sheet(), "csv")
#         else:
#             return HttpResponseBadRequest()
#     else:
#         form = UploadFileForm()
#     return render_to_response('upload_form.html',
#                               {'form': form},
#                               context_instance=RequestContext(request))

class LeaveAttendanceLog(models.Model):
	lev_id = models.ForeignKey('LeaveMaster', models.DO_NOTHING,null=True)
	action = models.CharField(max_length=250,blank=True,null=True)
	action_by =  models.CharField(max_length=200,blank=True,null=True)
	status = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)