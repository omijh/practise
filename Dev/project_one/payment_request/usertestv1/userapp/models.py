from django.db import models


# Models for userapp


# List of Countries with code
class CountryMaster(models.Model):

	country_name = models.CharField(max_length=100)
	country_iso_code = models.CharField(max_length=200,blank=True,null=True)
	country_isd_code = models.CharField(max_length=100,blank=True,null=True)
		

# List of Vertical 
class VerticalMaster(models.Model):

	vt_name = models.CharField(max_length=100)
	manager_name = models.CharField(max_length=200,blank=True,null=True)
	manager_email = models.CharField(max_length=100,blank=True,null=True)
	manager_code = models.CharField(max_length=100,blank=True,null=True)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.vt_name


# List of Regions
class RegionMaster(models.Model):

	rg_name = models.CharField(max_length=100)
	manager_name = models.CharField(max_length=200,blank=True,null=True)
	manager_email = models.CharField(max_length=100,blank=True,null=True)
	manager_code = models.CharField(max_length=100,blank=True,null=True)
	vertical_id = models.ForeignKey('VerticalMaster', models.DO_NOTHING,blank=True,null=True)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		manager_name = self.manager_name if self.manager_name else self.manager_email
		return manager_name


# List of Divisions
class DivisionMaster(models.Model):

	div_name = models.CharField(max_length=201)
	manager_name = models.CharField(max_length=200,blank=True,null=True)
	manager_email = models.CharField(max_length=100,blank=True,null=True)
	manager_code = models.CharField(max_length=100,blank=True,null=True)
	vertical_id = models.ForeignKey('VerticalMaster', models.DO_NOTHING,blank=True,null=True)
	region_id = models.ForeignKey('RegionMaster', models.DO_NOTHING,blank=True,null=True)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		manager_name = self.manager_name if self.manager_name else self.manager_email
		return manager_name


# List of Branch names
class BranchMaster(models.Model):
	
	br_name = models.CharField(max_length=45)
	br_pcof_id = models.IntegerField(blank=True, null=True)
	br_pcof_key = models.CharField(max_length=45, blank=True, null=True)
	manager_name = models.CharField(max_length=200,blank=True,null=True)
	manager_email = models.CharField(max_length=100,blank=True,null=True)
	manager_code = models.CharField(max_length=100,blank=True,null=True)
	vertical_id = models.ForeignKey('VerticalMaster', models.DO_NOTHING,blank=True,null=True)
	region_id = models.ForeignKey('RegionMaster', models.DO_NOTHING,blank=True,null=True)
	division_id = models.ForeignKey('DivisionMaster', models.DO_NOTHING,blank=True,null=True)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	cfo_name = models.CharField(max_length=50,default='Rahul Makhare', editable=False)
	cfo_email = models.CharField(max_length=50,default='rahul.makhare9@gmail.com', editable=False)
	def __str__(self):
		return self.br_name


# List of Designations
class DesignationMaster(models.Model):
	
	desg_name = models.CharField(max_length=150)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


# to store Details of Device allocated to employee
class DeviceAllocation(models.Model):

	device_name = models.CharField(max_length=45)
	serial_no = models.IntegerField()
	purchace_date = models.DateField()
	invoice_no = models.CharField(max_length=45)
	office_licence_no = models.CharField(max_length=45)
	windows_licence_no = models.CharField(max_length=45)
	emp_id = models.ForeignKey('EmployeeMaster', models.DO_NOTHING,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


def increment_request_id():

	last_request = RequestId.objects.all().order_by('id').last()
	if not last_request:
		return 'PCI' + '1000001'
	request_id = last_request.request_id
	request_int = int(request_id[3:])
	new_request_int = request_int + 1
	new_request_id = 'PCI' + str(new_request_int)
	return new_request_id


class RequestId(models.Model):

	request_id = models.CharField(unique=True, max_length=15, editable=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


# to store employee details
class EmployeeMaster(models.Model):

	# INPROCESS = 'In Process'
	# APPROVED = 'Approved'
	# REJECTED = 'Rejected'

	# EMP_STATUS_CHOICES = (
	# 	(INPROCESS, 'In Process'),
	# 	(APPROVED, 'Approved'),
	# 	(REJECTED, 'Rejected'),
	# )


	# request_id = models.CharField(unique=True, max_length=15)
	emp_code = models.CharField(unique=True, max_length=15)
	emp_fname = models.CharField(max_length=51, blank=True, null=True)
	emp_lname = models.CharField(max_length=51, blank=True, null=True)
	emp_email = models.CharField(unique=True, max_length=45, blank=True, null=True)
	country_isd_code = models.CharField(max_length=100,blank=True,null=True)
	emp_mobile = models.CharField(max_length=45)
	emp_address = models.CharField(max_length=45, blank=True, null=True)
	emp_dob = models.DateField(blank=True, null=True)
	# country = models.CharField(max_length=51,blank=True, null=True, default='India')
	country = models.ForeignKey(CountryMaster, models.DO_NOTHING,null=True,blank=True)
	date_of_joining = models.DateField(blank=True, null=True)

	master_table_id = models.IntegerField(max_length=45, blank=True, null=True)
	master_table_type = models.CharField(max_length=45, blank=True, null=True)

	reporting_authority = models.CharField(max_length=45, blank=True, null=True)
	reporting_authority_email = models.CharField(max_length=45, blank=True, null=True)

	activate = models.CharField(max_length=50,blank=True,null=True)
	deactivate =  models.CharField(max_length=50,blank=True,null=True)
	edit =  models.CharField(max_length=50,blank=True,null=True)
	
	emp_desg = models.ForeignKey(DesignationMaster, models.DO_NOTHING,null=True)
	request_id = models.ForeignKey(RequestId, models.DO_NOTHING,null=True)
	emp_status = models.CharField(max_length=101,blank=True, null=True)
	# emp_status = models.CharField(choices=EMP_STATUS_CHOICES, blank=True, null=True, max_length=51)
	company_email = models.CharField(max_length=101,blank=True, null=True)
	erp = models.BooleanField(default=False)
	anthil = models.BooleanField(default=False)
	lead_tracker = models.BooleanField(default=False)
	iauditor = models.BooleanField(default=False)
	dsp = models.BooleanField(default=False)
	service_track = models.BooleanField(default=False)
	navision = models.BooleanField(default=False)
	device_allocation = models.CharField(max_length=100)
	active = models.BooleanField(default=False)
	rejection_reason = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


# List of Apps
class AppMaster(models.Model):
	
	app_name = models.CharField(max_length=100)
	app_status = models.BooleanField(default=True)
	no_of_days = models.IntegerField(max_length=45, blank=True, null=True) 
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# app_admin = models.CharField(max_length=200)

	def __str__(self):
		return self.app_name


# to store App details assigned to employee
class EmpAppDetail(models.Model):
	# ACKNOWLEDGED = 'Acknowledged'
	# INPROCESS = 'In Process'
	# ACTIVE = 'Active'
	# INACTIVE = 'Inactive'

	# APP_STATUS_CHOICES = (
	# 	(ACKNOWLEDGED, 'Acknowledged'),
	# 	(INPROCESS, 'In Process'),
	# 	(ACTIVE, 'Active'),
	# 	(INACTIVE, 'Inactive'),
	# )
	
	app_login = models.CharField(max_length=101, blank=True, null=True)
	app_pass = models.CharField(max_length=101, blank=True, null=True)
	app_access_types = models.CharField(max_length=45, blank=True, null=True)
	ticket_no = models.CharField(max_length=101, blank=True, null=True)
	emp_app_status = models.CharField(max_length=45, default = 'Inactive')
	emp_id = models.ForeignKey('EmployeeMaster', models.DO_NOTHING,null=True)
	app_id = models.ForeignKey('AppMaster', models.DO_NOTHING, null=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)


# Table for App Admins
class AppAdmin(models.Model):
	
	app_id = models.ForeignKey('AppMaster', models.DO_NOTHING,null=True)
	admin_name = models.CharField(max_length=100)
	admin_status = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	email_id = models.CharField(max_length=100,blank=True,null=True)


# Table for App Roles
class AppRole(models.Model):
	
	app_id = models.ForeignKey('AppMaster', models.DO_NOTHING,null=True)
	role_name = models.CharField(max_length=100)
	role_status = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


# class TempNav(models.Model):
	
# 	app_id = models.ForeignKey('AppMaster', models.DO_NOTHING,null=True)
# 	request_id = models.ForeignKey('RequestId', models.DO_NOTHING,null=True)
# 	reference = models.CharField(max_length=100, null=True, blank=True)
# 	database_name = models.CharField(max_length=100, null=True, blank=True)
# 	company_book = models.CharField(max_length=100, null=True, blank=True)
# 	branch = models.CharField(max_length=100, null=True, blank=True)
# 	warehouse_location = models.CharField(max_length=100, null=True, blank=True)
# 	notes = models.CharField(max_length=500, null=True, blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)


class AppApprovalLog(models.Model):
	app_id = models.ForeignKey('AppMaster', models.DO_NOTHING,null=True)
	request_id = models.ForeignKey('RequestId', models.DO_NOTHING,null=True)
	action_by =  models.CharField(max_length=200,blank=True,null=True)
	mail_to = models.CharField(max_length=200,blank=True,null=True)
	mail_status = models.BooleanField(default=False,blank=True)
	approval_level = models.CharField(max_length=200,blank=True,null=True)
	approved = models.BooleanField(default=False,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# not in use
# class AppFieldMaster(models.Model):
# 	app_id = models.ForeignKey('AppMaster', models.DO_NOTHING,null=True)
# 	field_name = models.CharField(max_length=200,blank=True,null=True)
# 	field_order =  models.IntegerField(max_length=200,blank=True,null=True)
# 	field_status = models.BooleanField(default=True,blank=True)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True) 

class AppFieldValue(models.Model):
	app_id = models.ForeignKey('AppMaster', models.DO_NOTHING,null=True)
	emp_id = models.ForeignKey('EmployeeMaster', models.DO_NOTHING,null=True)
	field_name =  models.CharField(max_length=200,blank=True,null=True)
	field_value = models.CharField(max_length=500,blank=True,null=True)
	field_status = models.BooleanField(default=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)        	

class AppLog(models.Model):
	emp_id = models.ForeignKey('EmployeeMaster', models.DO_NOTHING,null=True)
	request_id = models.ForeignKey('RequestId', models.DO_NOTHING,null=True)
	action = models.CharField(max_length=250,blank=True,null=True)
	action_by =  models.CharField(max_length=200,blank=True,null=True)
	status = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)        


class AppApproverMaster(models.Model):
	app_id = models.ForeignKey('AppMaster', models.DO_NOTHING,null=True)
	approver_level = models.CharField(max_length=250,blank=True,null=True)
	approver_name =  models.CharField(max_length=200,blank=True,null=True)
	approver_email =  models.CharField(max_length=200,blank=True,null=True)
	status = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)        


class TempEmployeeMaster(models.Model):

	emp_code = models.CharField(unique=True, max_length=15)
	emp_fname = models.CharField(max_length=51, blank=True, null=True)
	emp_lname = models.CharField(max_length=51, blank=True, null=True)
	emp_email = models.CharField(unique=True, max_length=45, blank=True, null=True)
	country_isd_code = models.CharField(max_length=100,blank=True,null=True)
	emp_mobile = models.CharField(max_length=45)
	emp_address = models.CharField(max_length=45, blank=True, null=True)
	emp_dob = models.DateField(blank=True, null=True)
	country = models.ForeignKey(CountryMaster, models.DO_NOTHING,null=True,blank=True)
	date_of_joining = models.DateField(blank=True, null=True)

	master_table_id = models.IntegerField(max_length=45, blank=True, null=True)
	master_table_type = models.CharField(max_length=45, blank=True, null=True)

	reporting_authority = models.CharField(max_length=45, blank=True, null=True)
	reporting_authority_email = models.CharField(max_length=45, blank=True, null=True)
	
	emp_desg = models.ForeignKey(DesignationMaster, models.DO_NOTHING,null=True)
	emp_status = models.CharField(max_length=101,blank=True, null=True)
	company_email = models.CharField(max_length=101,blank=True, null=True)
	erp = models.BooleanField(default=False)
	anthil = models.BooleanField(default=False)
	lead_tracker = models.BooleanField(default=False)
	iauditor = models.BooleanField(default=False)
	dsp = models.BooleanField(default=False)
	service_track = models.BooleanField(default=False)
	navision = models.BooleanField(default=False)
	device_allocation = models.CharField(max_length=100)
	active = models.BooleanField(default=False)
	rejection_reason = models.TextField(null=True, blank=True)
	remark = models.CharField(max_length=45, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)	



class AppApprovalStatus(models.Model):
	app_id = models.ForeignKey('AppMaster', models.DO_NOTHING,null=True)
	emp_id = models.ForeignKey('EmployeeMaster', models.DO_NOTHING,null=True)
	request_id = models.ForeignKey('RequestId', models.DO_NOTHING,null=True)
	approver =  models.CharField(max_length=200,blank=True,null=True)
	approver_email =  models.CharField(max_length=200,blank=True,null=True)
	approval_level = models.CharField(max_length=200,blank=True,null=True)
	approval_status = models.CharField(max_length=200,blank=True,null=True)#PENDING,APPROVED,Rejected
	mail_status = models.BooleanField(default=False,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)