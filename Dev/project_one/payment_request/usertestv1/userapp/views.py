# views file for userapp

import re
import sys
import datetime
from django import template
from django.utils import timezone
from django.shortcuts import render,redirect
from django.utils.dateparse import parse_date
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from user_management.logger import log
from string import Template
from .custom_decorators import *
from .constant import *
from .models import * 
from .util import *

def whoami():
	'''
	to get current function name
	'''
	return sys._getframe(1).f_code.co_name

@login_required
def index(request):
	"""
	to show all employee records
	"""	
	# log.debug("Entering %s method" % (whoami()))  

	try:
	# 	log.info("Entering try block")

	# 	emps = EmployeeMaster.objects.order_by('-created_at')
	# 	verticals = VerticalMaster.objects.all()
	# 	regions = RegionMaster.objects.all()
	# 	divisions = DivisionMaster.objects.all()
	# 	branches = BranchMaster.objects.all()

	# 	if request.method == 'POST':
	# 		"""
	# 		Search function for employee list view using employee code,branch and status
	# 		"""

	# 		emp_br = request.POST.getlist('branch',False) or None
	# 		emp_status = request.POST.getlist('status',False) or None
	# 		emp_code = request.POST.get('emp_code',False) or None

	# 		if emp_br :
	# 			if emp_br[0]!="":
	# 				emp_br_objs = emps.filter(master_table_type='BRANCH')
	# 				emps = emp_br_objs.filter(master_table_id = str(emp_br[0]))

	# 		if emp_status :
	# 			if emp_status[0]!="":
	# 				emps = emps.filter(emp_status=emp_status[0])

	# 		if emp_code :
	# 			emps = emps.filter(emp_code=emp_code)
			
	# 	else:
	# 		emps = EmployeeMaster.objects.all()

	# 	branch_list = BranchMaster.objects.all()

	# 	context = {
	# 		'emps' : emps,
	# 		'verticals' : verticals,
	# 		'regions' : regions,
	# 		'branch_list' : branch_list,
	# 		'divisions' : divisions,
	# 		'branches' : branches,
	# 	}
		
		# return render(request, 'userapp/list_employee.html', context)
		return redirect('payment_request')
	except Exception as e: 
		log.exception(e)
		return render(request, 'userapp/page_404.html')	


# @group_required('service_now', redirect_url = 'add_employee')
@login_required
def employee_detail(request, emp_code):
	"""
	to show selected employee details(using emp_code)
	"""
	log.debug("Entering %s method" % (whoami()))
	try:
		log.debug("Entering try block")

		emp = EmployeeMaster.objects.get(emp_code = emp_code)
		apps = AppMaster.objects.all()
		
		app_details = {}

		for app in apps:
			emp_app_details = EmpAppDetail.objects.filter(emp_id=emp.id, app_id=app.id)
			if emp_app_details.exists():
				for emp_app_detail in emp_app_details:
					if emp_app_detail:
						app_details[app.app_name] = emp_app_detail.emp_app_status
			else:
				app_details[app.app_name] = 'Inactive'	

		
		vertical_list = VerticalMaster.objects.all()
		region_list = RegionMaster.objects.all()
		division_list = DivisionMaster.objects.all()
		branch_list = BranchMaster.objects.all()

		emp_master_id = emp.master_table_id
		master_table_type = emp.master_table_type

		vertical_id = None
		region_id = None
		division_id = None
		branch_id = None

		if master_table_type=='VERTICAL':
			vertical_id = VerticalMaster.objects.filter(id=emp_master_id).first()

		if master_table_type=='REGION':
			region_id = RegionMaster.objects.filter(id=emp_master_id).first()
			vertical_id = region_id.vertical_id

		if master_table_type=='DIVISION':
			division_id = DesignationMaster.objects.filter(id=emp_master_id).first()
			region_id = division_id.region_id
			vertical_id = region_id.vertical_id

		if master_table_type=='BRANCH':
			branch_id = BranchMaster.objects.filter(id=emp_master_id).first()
			if branch_id:
				division_id = branch_id.division_id
				if branch_id.vertical_id:
					vertical_id =branch_id.vertical_id
			if division_id :
				region_id = division_id.region_id
			if region_id:
				vertical_id = region_id.vertical_id
		
		designation_list = DesignationMaster.objects.all()
		branch_manager_list = []

		context = {
				'vertical_list':vertical_list,
				'region_list' : region_list,
				'division_list' : division_list,
				'branch_list' : branch_list,
				'emp_master_id':emp_master_id,
				'master_table_type':master_table_type,
				'designation_list' : designation_list,
				'emp': emp,
				'edit':True,
				'app_details':app_details,
				'branch_id' : branch_id,
				'division_id' : division_id,
				'region_id' : region_id,
				'vertical_id' : vertical_id
				}

		return render(request, 'userapp/employee_detail.html', context)
	except Exception as e: 
		log.exception(e)
		return redirect('index')	


@login_required
def add_employee(request):
	"""
		to add a new employee
		show master table details in form
	"""
	log.debug("Entering %s method" % (whoami()))
	try:
		log.debug("Entering try block")

		vertical_list = VerticalMaster.objects.all()
		region_list = RegionMaster.objects.all()
		division_list = DivisionMaster.objects.all()
		branch_list = BranchMaster.objects.all()
		department_list =[]
		designation_list = DesignationMaster.objects.all()
		country_list = CountryMaster.objects.all()
		
		context = {
		'vertical_list' : vertical_list,
		'region_list' : region_list,
		'division_list' : division_list,
		'branch_list' : branch_list,
		'department_list' : department_list,
		'designation_list' : designation_list,
		'country_list':country_list,
		}

		return render(request, 'userapp/add_employee.html', context)

	except Exception as e: 
		log.exception(e)
		return redirect('index')	


def drop_down_list(request):
	"""
	drop down lists for Vertical, Region, Division, Branch using ajax
	"""
	log.debug("Entering %s method" % (whoami()))
	try:
		log.debug("Entering try block")

		log.info("In test app .....................................")
		selected_id = request.GET.get('data_id')
		drop_down_type = request.GET.get('type')
		log.info("In test app .....................................{}=={}".format(selected_id,drop_down_type))

		if drop_down_type =='branch':
			region_list = RegionMaster.objects.filter(vertical_id=selected_id)
			div_list = DivisionMaster.objects.filter(region_id__in= region_list)
				
			log.info("BranchMaster.............................")
			branch_list = BranchMaster.objects.filter(division_id__in= div_list)

		if drop_down_type=='branch_list':
			data={}
			branch_list = BranchMaster.objects.filter(id= selected_id).first()

			if branch_list:

				data={

				"division" : {
					"name":branch_list.division_id.div_name,
					"id":branch_list.division_id.id
					},

				"region" : {
					"name":branch_list.division_id.region_id.rg_name,
					"id":branch_list.division_id.region_id.id
					}

				}
					
				return JsonResponse(data)
				
		drop_down_type='branch'

		return render(request, 'userapp/drop_down_view.html', {'data_list': branch_list,'drop_down_type':drop_down_type})
	except Exception as e:
		log.exception(e)
		return redirect('index')


@login_required
def save_employee(request):
	"""
		to save employee data and redirect page to list view
	"""
	log.debug("Entering %s method" % (whoami()))
	try:
		log.debug("Entering try block")

		if request.method == 'POST':
			
			emp_code = request.POST.get('emp_code',None)
			first_name = request.POST.get('first_name',None)
			last_name = request.POST.get('last_name',None)
			dob_str = request.POST.get('dob',None)
			email_id = request.POST.get('email_id',None)
			contact_num = request.POST.get('contact_num',None)
			emp_address = request.POST.get('emp_address',None)
			doj_str = request.POST.get('doj',None)
			country = request.POST.get('country',None)

			authority = request.POST.get('authority',None)
			authority_email = request.POST.get('authority_email',None)

			vertical = request.POST.getlist('vertical') or None
			region = request.POST.getlist('region') or None
			division = request.POST.getlist('division') or None
			branch = request.POST.getlist('branch') or None
			designation = request.POST.getlist('designation') or None

			emp_ins = EmployeeMaster()

			if vertical :
				if not vertical[0] in [str("None"),""]:
					vertical_ins = VerticalMaster.objects.filter(id=vertical[0]).first()
					if vertical_ins is not None:
						emp_ins.master_table_id = vertical_ins.id
						emp_ins.master_table_type = 'VERTICAL'

			if region  :
				if not region[0] in [str("None"),""] : 
					region_ins = RegionMaster.objects.filter(id=region[0]).first()
					if region_ins is not None:
						emp_ins.master_table_id = region_ins.id
						emp_ins.master_table_type = 'REGION'

			if division :
				if  not division[0] in [str("None"),""]:
					division_ins = DivisionMaster.objects.filter(id=division[0]).first()
					if division_ins is not None:
						emp_ins.master_table_id = division_ins.id
						emp_ins.master_table_type = 'DIVISION'

			if branch :
				if not branch[0] in [str("None"),""]:
					branch_ins = BranchMaster.objects.filter(id = branch[0]).first()
					if branch_ins :
						emp_ins.master_table_id = branch_ins.id
						emp_ins.master_table_type = 'BRANCH'

			if designation :
				if not designation[0] == str("None") :
					designation_ins = DesignationMaster.objects.get(id = designation[0])
					if  designation_ins:
						emp_ins.emp_desg_id = designation_ins.id
			
			# to create request ID for employee 
			req_ins = RequestId()

			last_request = RequestId.objects.all().order_by('id').last()
			if not last_request:
				new_request_id = 'PCI' + '1000001'
			else:	
				request_id = last_request.request_id
				request_int = int(request_id[3:])
				new_request_int = request_int + 1
				new_request_id = 'PCI' + str(new_request_int)

			req_ins.request_id = new_request_id
			req_ins.save()

			emp_ins.request_id = req_ins	
			emp_dob = parse_date(dob_str)
			emp_doj = parse_date(doj_str)

			emp_status = 'In Process'

			if emp_code is not None:
				emp_ins.emp_code = emp_code

			if first_name is not None:
				emp_ins.emp_fname = first_name

			if last_name is not None:
				emp_ins.emp_lname = last_name

			if emp_dob is not None:
				emp_ins.emp_dob = emp_dob

			if email_id is not None:
				emp_ins.emp_email = email_id

			if contact_num is not None:
				emp_ins.emp_mobile = contact_num

			if emp_address is not None:
				emp_ins.emp_address = emp_address

			if emp_doj is not None:
				emp_ins.date_of_joining = emp_doj

			if emp_status is not None:
				emp_ins.emp_status = emp_status

			if authority is not None:
				emp_ins.reporting_authority = authority	

			if authority_email is not None:
				emp_ins.reporting_authority_email = authority_email		

			if country is not None:
				country = CountryMaster.objects.get(id = country)
				emp_ins.country = country
				emp_ins.country_isd_code = 	country.country_isd_code

			emp_ins.save()

			# to create log for employee add action
			log_obj = AppLogCl(emp_ins.id)
			action="Employee created"
			action_by = request.user.username
			log_obj.create_log(action,action_by)

			# to send email to reporting authority for employee approval
			to_mail = authority_email
			ip = HOST
			msub="Employee approve mail"
			mbody="Please click on below link to Approve/Disapprove Employee & provide Application Access Rights http://{0}/employee_approval/{1}".format(ip,emp_ins.emp_code)
			mail_to_bm(request,emp_ins,to_mail)

		else :
			pass
		return redirect('index')	
	except Exception as e: 
		log.exception(e)
		return redirect('index')	


def employee_approval(request, emp_code):
	"""
	to show employee details to manager to approve/reject employee
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp = EmployeeMaster.objects.get(emp_code = emp_code)
		apps = AppMaster.objects.all()
		approles = AppRole.objects.filter(role_status = True)

		location_type = emp.master_table_type

		if location_type == 'VERTICAL':
			location = VerticalMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type == 'REGION':
			location = RegionMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type == 'DIVISION':
			location = DivisionMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type =='BRANCH':
			location = BranchMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		
		designation_list = DesignationMaster.objects.all()
		branch_manager_list = []

		context = {
				'emp': emp,
				'apps':apps,
				'approles':approles,
				'location_type':location_type,
				'location':location,
				'manager':manager
				}

		return render(request, 'userapp/employee_approval_form.html', context)

	except Exception as e: 
		log.exception(e)
		print("Exception :",e)
		return redirect('index')	


def reject_employee(request):
	"""
	to send reject employee email to service now and update emp status
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		if request.method == 'POST':

			emp_code = request.POST['emp_code']
			reason = request.POST['reason']
			manager = request.POST.get("manager")

			emp_obj = EmployeeMaster.objects.get(emp_code=emp_code)

			EmployeeMaster.objects.filter(emp_code=emp_code).update(emp_status='Rejected', rejection_reason=reason)

			msub="Employee {} {} got rejected".format(emp_obj.emp_fname, emp_obj.emp_lname)
			mbody="Employee Details : {}, {}, {}  is rejected by Branch Manager {}. Reason: {}.".format(emp_obj.emp_code,emp_obj.emp_fname,emp_obj.emp_desg.desg_name,manager,reason)
			mto = SYSMAIL
			mfrom=SYSMAIL
			app_task(args=(msub,mbody,mfrom,mto))

			# to create log for reject employee action
			action_by=None
			if manager:
				action_by = manager
			log_obj = AppLogCl(emp_obj.id)
			action="Employee rejected by reporting authority"
			log_obj.create_log(action,action_by)
		else :
			pass	
		return render(request, 'userapp/thank_you.html')

	except Exception as e: 
		log.exception(e)
		return redirect('index')		


def approve_employee(request):
	"""
	to send approve employee email to service now and update emp status
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")

		if request.method == 'POST':

			emp_code = request.POST.get('emp_code')
			app_list = request.POST.getlist("apps")
			app_roles = request.POST.getlist("apps_role")
			manager = request.POST.get("manager")

			emp_obj = EmployeeMaster.objects.get(emp_code=emp_code)

			EmployeeMaster.objects.filter(emp_code=emp_code).update(emp_status='Approved', active= True)

			app_dict = {}

			for app_role in app_roles:
				log.info('app_role %s' %(app_role))

				app_rr = AppRole.objects.get(id = app_role)
				log.info('app_rr %s' %(app_rr))

				if EmpAppDetail.objects.filter(app_id = app_rr.app_id, emp_id = emp_obj).exists():	
					app_dict[app_rr.app_id.app_name] = 'Mail has already been sent'
					log.info('app_dict %s' %(app_dict))

				else:	
					emp_app_obj= EmpAppDetail()
					emp_app_obj.emp_app_status = ACKL
					emp_app_obj.emp_id = emp_obj
					emp_app_obj.app_access_types = app_rr.role_name
					emp_app_obj.app_id = app_rr.app_id
					emp_app_obj.save()

					app_dict[app_rr.app_id.app_name] = 'Mail sent for app creation request'
					log.info('app_dict2 %s' %(app_dict))

					# Gamil
					if app_rr.app_id.app_name=='Gmail':
						log.info('Mail to gmail ..')

						g_obj=GmailApp(emp_obj.id,app_rr.app_id.id)
						st=g_obj.approval_1()

						if st:
							g_obj.app_approval_status(level=1,status='PENDING')
						else:
							g_obj.app_approval_status(level=1,status='FAILED')
						
					# Erp App
					elif app_rr.app_id.app_name=='ERP':
						log.info('Mail to erp ..')

						erp_obj=ErpApp(emp_obj.id,app_rr.app_id.id)
						st=erp_obj.approval_1()

						if st:
							erp_obj.app_approval_status(level=1,status='PENDING')
						else:
							erp_obj.app_approval_status(level=1,status='FAILED')

					# Anthil App
					elif app_rr.app_id.app_name=='Anthil':
						log.info('Mail to anthil ..')

						anthil_obj=AnthilApp(emp_obj.id,app_rr.app_id.id)
						st=anthil_obj.approval_1()

						if st:
							anthil_obj.app_approval_status(level=1,status='PENDING')
						else:
							anthil_obj.app_approval_status(level=1,status='FAILED')

					# Anthil App
					elif app_rr.app_id.app_name  == 'Navision':
						log.info('Mail to nav ..')

						app_obj=NavApp(emp_obj.id,app_rr.app_id.id)
						st=app_obj.approval_1()

						if st:
							app_obj.app_approval_status(level=1,status='PENDING')
						else:
							app_obj.app_approval_status(level=1,status='FAILED')

					# Anthil App
					elif app_rr.app_id.app_name  == 'iCABS':
						log.info('Mail to icabs ..')

						icab_obj=ICabsApp(emp_obj.id,app_rr.app_id.id)
						st=icab_obj.approval_1()

						if st:
							icab_obj.app_approval_status(level=1,status='PENDING')
						else:
							icab_obj.app_approval_status(level=1,status='FAILED')

					# DSP App 
					elif app_rr.app_id.app_name  == 'DSP':
						log.info('Mail to DSP ..')

						dsp_obj=DspApp(emp_obj.id,app_rr.app_id.id)
						st=dsp_obj.approval_1()

						if st:
							pass
						else:
							dsp_obj.app_approval_status(level=1,status='FAILED')
						
					# Service Tracker App 
					elif app_rr.app_id.app_name  == 'Service Tracker':
						log.info('Mail to Service tracker ..')

						st_obj=STPApp(emp_obj.id,app_rr.app_id.id)
						st=st_obj.approval_1()

						if st:
							st_obj.app_approval_status(level=1,status='PENDING')
						else:
							st_obj.app_approval_status(level=1,status='FAILED')
							
					# iAuditor App 
					elif app_rr.app_id.app_name  == 'iAuditor':
						log.info('Mail to Service tracker ..')

						iaud_obj=iAuditorApp(emp_obj.id,app_rr.app_id.id)
						st=iaud_obj.approval_1()
						log.info('iAuditor %s' %(st))

						if st:
							iaud_obj.app_approval_status(level=1,status='PENDING')
						else:
							log.info("In False iaudior")
							iaud_obj.app_approval_status(level=1,status='FAILED')

					# SPA App
					elif app_rr.app_id.app_name=='SPA':
						log.info('Mail to SPA ..')

						spa_obj=SPAApp(emp_obj.id,app_rr.app_id.id)
						st=spa_obj.approval_1()

						if st:
							pass
						else:
							spa_obj.app_approval_status(level=1,status='FAILED')		

					# for any other app 
					else:	

						url = "http://{}/emp_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_obj.id)
						msub="Employee {} {} got approved".format(emp_obj.emp_fname, emp_obj.emp_lname)
						mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see emp app detail {}".format(emp_obj.request_id,app_rr.app_id.app_name,app_rr.role_name,emp_obj.emp_code,emp_obj.emp_fname,emp_obj.emp_lname,emp_obj.emp_mobile,emp_obj.emp_email,url)
						mto =SYSMAIL
						mfrom=SYSMAIL
						app_task(args=(msub,mbody,mfrom,mto))

			log.info('app_dict3 %s' %(app_dict))

			# log for employee approve
			action_by=None
			if manager:
				action_by = manager
			log_obj = AppLogCl(emp_obj.id)
			action="Employee approved by reporting authority"
			log_obj.create_log(action,action_by)

			context = {'app_dict':app_dict}

		else :
			pass	

		return render(request, 'userapp/thank_you2.html' ,context )

	except Exception as e: 
		log.exception(e)
		return redirect('index')	


@login_required
def app_account_list(request):
	"""
	List of all employees who has been approved or rejected by branch manager in URL - app_account_list.
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		apps = EmpAppDetail.objects.values('emp_id').distinct()
		app_list = []
		app_master = ''
		dist = {}
		for app in apps:
			emp = EmployeeMaster.objects.get(id=app.get('emp_id'))
			if emp.emp_status == 'Active' or emp.emp_status == 'Rejected' :
				location_type = emp.master_table_type
				if location_type == 'VERTICAL':
					location = VerticalMaster.objects.get(id = emp.master_table_id)
				elif location_type == 'REGION':
					location = RegionMaster.objects.get(id = emp.master_table_id)
				elif location_type == 'DIVISION':
					location = DivisionMaster.objects.get(id = emp.master_table_id)
				elif location_type =='BRANCH':
					location = BranchMaster.objects.get(id = emp.master_table_id)

				dist = {'emp_code': emp.emp_code ,'fname': emp.emp_fname ,'lname': emp.emp_lname,'master_table_type': emp.master_table_type,'location':location,'email': emp.emp_email ,'desg':emp.emp_desg.desg_name ,'status':emp.emp_status }
				app_master = AppMaster.objects.all()
				log.info('app_master %s' %(app_master))
				for master in app_master:
					log.info('master %s' %(master))
					app_value = EmpAppDetail.objects.filter(emp_id=emp.id,app_id=master.id)
					if len(app_value) > 0 :
						for app_val in app_value:
							dist[str(master.app_name)] = app_val.emp_app_status
				app_list.append(dist)
				log.info('app_list %s' %(app_list))

		return render(request, 'userapp/app_account_list.html', {'apps':app_list,'master':app_master})

	except Exception as e: 
		log.exception(e)
		return redirect('index')
			

@login_required
def app_account_form(request,emp_code):
	"""
	To View Application Account Details while clicking on Emp Code in app_account_list View.
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp = EmployeeMaster.objects.get(emp_code = emp_code)
		emp_app_ins = EmpAppDetail.objects.filter(emp_id=emp)
		emp_app_list=[]
		emp=''

		for emp_app in emp_app_ins:
			app_dict={}
			emp=emp_app.emp_id
			
			if emp_app.emp_app_status in ['Acknowledged','Active','In Process']:
				app_dict['app_name'] = emp_app.app_id.app_name
				app_dict['id'] = emp_app.id
				app_dict['role'] = emp_app.app_access_types
				app_dict['status'] = emp_app.emp_app_status
				app_dict['app_id'] = emp_app.app_id
				app_dict['emp_id'] = emp_app.emp_id
				app_dict['app_login'] = emp_app.app_login
				emp_app_list.append(app_dict)

		vertical_list = VerticalMaster.objects.all()
		region_list = RegionMaster.objects.all()
		division_list = DivisionMaster.objects.all()
		branch_list = BranchMaster.objects.all()

		emp_master_id = emp.master_table_id
		master_table_type = emp.master_table_type

		vertical_id = None
		region_id = None
		division_id = None
		branch_id = None

		if master_table_type=='VERTICAL':
			vertical_id = VerticalMaster.objects.filter(id=emp_master_id).first()

		if master_table_type=='REGION':
			region_id = RegionMaster.objects.filter(id=emp_master_id).first()
			vertical_id = region_id.vertical_id

		if master_table_type=='DIVISION':
			division_id = DesignationMaster.objects.filter(id=emp_master_id).first()
			region_id = division_id.region_id
			vertical_id = region_id.vertical_id

		if master_table_type=='BRANCH':
			branch_id = BranchMaster.objects.filter(id=emp_master_id).first()
			division_id = branch_id.division_id
			region_id = division_id.region_id
			vertical_id = region_id.vertical_id
		
		designation_list = DesignationMaster.objects.all()
		branch_manager_list = []

		context = {
				'vertical_list':vertical_list,
				'region_list' : region_list,
				'division_list' : division_list,
				'branch_list' : branch_list,
				'emp_master_id':emp_master_id,
				'master_table_type':master_table_type,
				'emp': emp,
				'branch_id' : branch_id,
				'division_id' : division_id,
				'region_id' : region_id,
				'vertical_id' : vertical_id,
				'emp_app_list':emp_app_list
				}
		return render(request, 'userapp/app_account_form.html', context)	

	except Exception as e: 
		log.exception(e)
		return redirect('index')	
			

def edit_emp_app(request, emp_app_detail_id):
	"""
	to save employee app detail (login credential for each app)
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")

		if request.method == 'POST':
			app_user_name = request.POST.get('app_user_name',None)
			app_pswd = request.POST.get('app_pass',None)
			app = request.POST.get('app_1',None)
			emp_fname = request.POST.get('emp_fname',None)
			emp_lname = request.POST.get('emp_lname',None)
			ticket_no = request.POST.get("ticket_no",None)

		if app_user_name is not None and emp_app_detail_id is not None:

			emp_app_detail_ins = EmpAppDetail.objects.filter(id=emp_app_detail_id).first()
			emp_app_detail_ins.app_login=app_user_name
			emp_app_detail_ins.emp_app_status='Active'

			if ticket_no:
				emp_app_detail_ins.ticket_no=ticket_no

			emp_app_detail_ins.save()

			# Gmail
			if emp_app_detail_ins:

				if emp_app_detail_ins.app_id.id == 1:

					app_obj=GmailApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
					app_obj.app_approval_status(level=2,status='APPROVED')
					st= app_obj.approval_3()

					if st:
						pass
						
					else:
						app_obj.app_approval_status(level=2,status='FAILED')

				if emp_app_detail_ins.app_id.id == 11:

					app_obj=AnthilApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
					app_obj.app_approval_status(level=2,status='APPROVED')

					st= app_obj.approval_3()

					if st:
						pass
						
					else:
						app_obj.app_approval_status(level=3,status='FAILED')
					
				if emp_app_detail_ins.app_id.id == 2:

					erp_obj=ErpApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
					erp_obj.app_approval_status(level=2,status='APPROVED')

					st= erp_obj.approval_3()

					if st:
						pass
						
					else:
						app_obj.app_approval_status(level=3,status='FAILED')

				if emp_app_detail_ins.app_id.id == 7:

					nav_obj=NavApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
					nav_obj.app_approval_status(level=2,status='APPROVED')
					st= nav_obj.approval_3()

					if st:
						pass
						
					else:
						nav_obj.app_approval_status(level=3,status='FAILED')

				if emp_app_detail_ins.app_id.app_name == 'iAuditor':

					nav_obj=iAuditorApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
					nav_obj.app_approval_status(level=1,status='APPROVED')
					st= nav_obj.approval_2()

					if st:
						pass
						
					else:
						nav_obj.app_approval_status(level=2,status='FAILED')

				if emp_app_detail_ins.app_id.app_name =='SPA':

					app_obj=SPAApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
					app_obj.app_approval_status(level=2,status='APPROVED')
					st= app_obj.approval_3()

					if st:
						pass
						
					else:
						app_obj.app_approval_status(level=2,status='FAILED')

			else :

				ip = HOST

				mbody="This is to inform you that Employees Account for Application :{0} has been Activated with User Name :{1} & Password : {2}".format(app,app_user_name,app_pswd)
				to_mail =SYSMAIL
				mail_to_service_now(request,to_mail,mbody)

			return render(request, 'userapp/thank_you1.html')

		return redirect('index')	

	except Exception as e: 
		log.exception(e)
		return redirect('index') 


def emp_app_detail(request, emp_app_detail):
	"""
	to send employee details to app admin to create app account
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp_app_detail_obj = EmpAppDetail.objects.get(id = emp_app_detail)

		return render(request, 'userapp/emp_app_detail.html', {'emp_app_detail_obj': emp_app_detail_obj})

	except Exception as e: 
		log.exception(e)
		return redirect('index')	


@login_required
def validate_emp_code(request):
	"""
	to check if emp_code already exist in database or not
	unique emp_code validation front end
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp_code = request.GET.get('emp_code', None)
		data = {
			'is_taken': EmployeeMaster.objects.filter(emp_code=emp_code).exists()
		}
		return JsonResponse(data)
	except Exception as e:
		log.exception(e)
		print("Exception :",e)
		return redirect('index')


@login_required
def validate_email_id(request):
	"""
	to check if personal email id already exist in database or not
	unique personal email id validation front end
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		email_id = request.GET.get('email_id', None)
		data = {
			'is_taken': EmployeeMaster.objects.filter(emp_email=email_id).exists()
		}
		return JsonResponse(data)
	except Exception as e:
		log.exception(e)
		print("Exception :",e)
		return redirect('index')


def select_country_ext(request):
	"""
	to auto select country ext for selected country from database
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		country = request.GET.get('country')
		code = CountryMaster.objects.values('country_isd_code').get(id=country)
		data = {
			'ext': '+' + code.get('country_isd_code')
		}
		return JsonResponse(data)
	except Exception as e:
		log.exception(e)
		return redirect('index')
		

def nav_access_approval(request, emp_code,app_id):
	"""
	to send employee details to manager to approve/reject employee
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp = EmployeeMaster.objects.filter(emp_code = emp_code).first()
		apps = AppMaster.objects.filter(id=app_id)
		emp_app_detail = EmpAppDetail.objects.filter(app_id=apps,emp_id=emp).first()
		approles = AppRole.objects.all()

		location_type = emp.master_table_type

		if location_type == 'VERTICAL':
			location = VerticalMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type == 'REGION':
			location = RegionMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type == 'DIVISION':
			location = DivisionMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type =='BRANCH':
			location = BranchMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		
		designation_list = DesignationMaster.objects.all()

		context = {
				'emp': emp,
				'apps':apps,
				'approles':approles,
				'location_type':location_type,
				'location':location,
				'manager':manager,
				'emp_app':apps[0],
				'emp_app_detail':emp_app_detail
				}

		return render(request, 'userapp/app_approval/nav_access_approval_form.html', context)

	except Exception as e:
		log.exception(e) 
		return redirect('index')


def save_nav_access_approval(request):
	'''
	to save details entered by nav approvar
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		fields =  {}

		request_id = request.POST.get('request_id')
		emp_app_detail_id = request.POST.get('emp_app_detail_id')

		fields['Database Name'] = request.POST.get('database_name')
		fields['Company Book'] = request.POST.get('company_book')
		fields['Branch'] = request.POST.get('nav_branch')
		fields['Warehouse Location'] = request.POST.get('warehouse_location')
		fields['Notes'] = request.POST.get('notes')
		fields['Reference'] = request.POST.get('reference')

		emp_app_detail_ins = EmpAppDetail.objects.get(id=emp_app_detail_id)
		app_ins = emp_app_detail_ins.app_id
		emp_ins = emp_app_detail_ins.emp_id

		for key,value in fields.items():
			field_obj = AppFieldValue()	
			field_obj.app_id = app_ins
			field_obj.emp_id = emp_ins
			field_obj.field_name = key
			field_obj.field_value = value
			field_obj.save()

		nav_obj=NavApp(emp_ins.id,app_ins.id)
		
		nav_obj.app_approval_status(level=1,status='APPROVED')

		approval_level = '2'
		r = nav_obj.mail_to_sn(action=approval_level)  # New account creation request

		if r:
			nav_obj.app_approval_status(level=2,status='PENDING')
			
		else:
			nav_obj.app_approval_status(level=2,status='FAILED')

		return render(request, 'userapp/thank_you.html')
	except Exception as e:
		log.exception(e) 
		return redirect('index')	


def nav_app_detail(request, emp_app_detail):
	"""
	to send employee details and navision details to Service Now to create app account
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp_app_detail = EmpAppDetail.objects.get(id =emp_app_detail)
		emp_ins = EmployeeMaster.objects.get(id = emp_app_detail.emp_id.id)
		app_ins = AppMaster.objects.get(id = emp_app_detail.app_id.id)
		navs = AppFieldValue.objects.filter(app_id = emp_app_detail.app_id.id, emp_id = emp_app_detail.emp_id.id)

		nav_dict ={}
		for nav in navs:
			nav_dict[nav.field_name] = nav.field_value

		location_type = emp_ins.master_table_type

		if location_type == 'VERTICAL':
			location = VerticalMaster.objects.get(id = emp_ins.master_table_id)
		elif location_type == 'REGION':
			location = RegionMaster.objects.get(id = emp_ins.master_table_id)
		elif location_type == 'DIVISION':
			location = DivisionMaster.objects.get(id = emp_ins.master_table_id)
		elif location_type =='BRANCH':
			location = BranchMaster.objects.get(id = emp_ins.master_table_id)

		context = {
			'emp':emp_ins,
			'app':app_ins,
			'nav_dict':nav_dict,
			'emp_app_detail':emp_app_detail,
			'location':location,
			'location_type':location_type,
		}

		nav_obj=NavApp(emp_ins.id, app_ins.id)
		approval_level = '3'
		nav_obj.app_approval_status(level=2,status='APPROVED')
		st= nav_obj.mail_to_sn(action =approval_level)

		if st:
			pass	
		else:
			nav_obj.app_approval_status(level=3,status='FAILED')
		
		return render(request, 'userapp/app_approval/nav_app_detail_form.html', context)
	except Exception as e: 
		log.exception(e)
		return redirect('index')               

####################################################################################################

@login_required
def emp_log_list(request,emp_code):
	'''
	logs for employee (using emp_code) 
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		
		emp_ins=EmployeeMaster.objects.filter(emp_code=emp_code).first()

		log_list = AppLog.objects.filter(emp_id=emp_ins)

		fullname=None
		request_id = emp_ins.request_id.request_id or ""
		if emp_ins.emp_fname:
			fullname =  emp_ins.emp_fname
		if emp_ins.emp_lname:
			fullname = str(fullname +" "+ emp_ins.emp_lname)

		context={
			'log_list':log_list,
			'emp_code':emp_ins.emp_code,
			'request_id':request_id,
			'emp_name':str(fullname)
		}

		return render(request, 'userapp/emp_log_list.html', context)
	except Exception as e: 
		log.exception(e)
		return redirect('index')


def reject_app_info(request,emp_app_detail):
	''' 
	to save reject info
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")

		if emp_app_detail:
			reason = request.POST.get('reason')
			emp_app_detail_ins = EmpAppDetail.objects.filter(id=emp_app_detail).first()
			emp_app_detail_ins.emp_app_status=APP_REJECTED
			emp_app_detail_ins.save()

			return render(request, 'userapp/thank_you.html')

	except Exception as e:
		log.exception(e)
		return redirect('')


def approve_app_info(request,emp_app_detail):
	'''
	to save approve app info
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp_app_detail_ins = EmpAppDetail.objects.filter(id=emp_app_detail).first()
		if emp_app_detail_ins.app_id.app_name=='Gmail':

			app_obj = GmailApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
			app_obj.app_approval_status(level=1,status='APPROVED')
			
			st=app_obj.approval_2()

			if st:
				app_obj.app_approval_status(level=2,status='PENDING')
				
			else:
				app_obj.app_approval_status(level=2,status='FAILED')

		if emp_app_detail_ins.app_id.app_name=='Anthil':

			app_obj = AnthilApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
			app_obj.app_approval_status(level=1,status='APPROVED')
			
			st=app_obj.approval_2()

			if st:
				app_obj.app_approval_status(level=2,status='PENDING')
				
			else:
				app_obj.app_approval_status(level=2,status='FAILED')

		if emp_app_detail_ins.app_id.app_name=='ERP':

			app_obj = ErpApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
			app_obj.app_approval_status(level=1,status='APPROVED')
			st=app_obj.approval_2()

			if st:
				app_obj.app_approval_status(level=2,status='PENDING')
				
			else:
				app_obj.app_approval_status(level=2,status='FAILED')

		if emp_app_detail_ins.app_id.app_name=='iCABS':

			app_obj = ICabsApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
			app_obj.app_approval_status(level=1,status='APPROVED')
			
			st=app_obj.approval_2()

			if st:
				app_obj.app_approval_status(level=2,status='PENDING')
				
			else:
				app_obj.app_approval_status(level=2,status='FAILED')

		return render(request, 'userapp/thank_you.html')

	except Exception as e:
		log.exception(e)
		return redirect('index')


def stp_app_2(request,emp_app_detail):

	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp_app_detail_ins = EmpAppDetail.objects.filter(id=emp_app_detail).first()
		field_obj = AppFieldValue.objects.filter(emp_id=emp_app_detail_ins.emp_id,app_id=emp_app_detail_ins.app_id,field_name='Service Area').first()

		if field_obj.field_name:

			service_area =  field_obj.field_name

		return render(request, 'userapp/app_approval/app_stp_detail.html', {'emp_app_detail_obj': emp_app_detail_ins,'service_area':service_area})
	except Exception as e:
		log.exception(e)
		return redirect('index')
	

def stp_app_view(request,emp_app_detail):
	'''
	to show stp app approval form
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp_app_detail_obj = EmpAppDetail.objects.get(id = emp_app_detail)
		emp_app_detail_ins = EmpAppDetail.objects.filter(id=emp_app_detail).first()

		return render(request, 'userapp/app_approval/stp_app_form.html', {'emp_app_detail_obj': emp_app_detail_obj})

	except Exception as e:
		log.exception(e)
		return redirect('index')


def stp_app_save(request,emp_app_detail):
	'''
	to save stp app detail
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		fields={}
		emp_app_detail_ins = EmpAppDetail.objects.get(id = emp_app_detail)
		fields['Service Area'] = request.POST.get('service_area',None)

		for key,value in fields.items():
			field_obj = AppFieldValue()    
			field_obj.app_id = emp_app_detail_ins.app_id
			field_obj.emp_id = emp_app_detail_ins.emp_id
			field_obj.field_name = key
			field_obj.field_value = value
			field_obj.save()

		stp_ins = STPApp(emp_app_detail_ins.emp_id.id,emp_app_detail_ins.app_id.id)
		stp_ins.app_approval_status(level=1,status='APPROVED')
		
		st=stp_ins.approval_2() # Second approval process
						
		if st:
			stp_ins.app_approval_status(level=2,status='PENDING')
		else:
			stp_ins.app_approval_status(level=2,status='FAILED')
		
		return render(request, 'userapp/thank_you.html')

	except Exception as e:
		log.exception(e)
		return redirect('index')


def dsp_app_detail(request,emp_app_detail):
	"""
	to send employee details to DSP app admin to create app account
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp_app_detail_ins = EmpAppDetail.objects.get(id = emp_app_detail)

		master_table_id=emp_app_detail_ins.emp_id.master_table_id
		master_table_type=emp_app_detail_ins.emp_id.master_table_type
		mater_table=LocationCl(master_table_id,master_table_type)
		location = mater_table.getLocation()
		
		context={
			'emp':emp_app_detail_ins.emp_id,
			'emp_app_detail':emp_app_detail_ins,
			'location_type':location['location_type'],
			'location_name':location['location_name']
		}

		return render(request, 'userapp/app_approval/dsp_access_approval_form.html',context)

	except Exception as e:
		log.exception(e)
		return redirect('index')


def save_dsp_access_detail(request,emp_app_detail):
	'''
	to save dsp app detail
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")

		fields = {}
		emp_app_detail_ins = EmpAppDetail.objects.filter(id=emp_app_detail).first()
		app_ins = emp_app_detail_ins.app_id
		emp_ins = emp_app_detail_ins.emp_id

		app_user_name = None

		fields['Sales Manager'] = request.POST.get('sales_manager',None)
		fields['Sales Manager Email'] = request.POST.get('sales_manager_email',None)
		fields['Business Manager'] = request.POST.get('business_manager',None)
		fields['Business Manager Email'] = request.POST.get('business_manager_email',None)
		fields['Division'] = request.POST.get('division',None)
		ticket_no = request.POST.get('ticket_no',None)

		emp_app_detail_ins.app_login=app_user_name
		emp_app_detail_ins.emp_app_status=ACTIVE

		if ticket_no:
			emp_app_detail_ins.ticket_no=ticket_no

		emp_app_detail_ins.save()
		
		for key,value in fields.items():

			field_obj = AppFieldValue()    
			field_obj.app_id = app_ins
			field_obj.emp_id = emp_ins
			field_obj.field_name = key
			field_obj.field_value = value
			field_obj.save()

		dsp_ins=DspApp(emp_ins.id,app_ins.id)

		dsp_ins.app_approval_status(level=2,status='APPROVED')
		dsp_ins.approval_3()

		return render(request, 'userapp/thank_you.html')

	except Exception as e:
		log.exception(e)
		return render(request, 'userapp/page_500.html')


def spa_app_detail(request,emp_app_detail):
	"""
	to send employee details to SPA app admin to create app account
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp_app_detail_ins = EmpAppDetail.objects.get(id = emp_app_detail)

		master_table_id=emp_app_detail_ins.emp_id.master_table_id
		master_table_type=emp_app_detail_ins.emp_id.master_table_type
		mater_table=LocationCl(master_table_id,master_table_type)
		location = mater_table.getLocation()
		
		context={
			'emp':emp_app_detail_ins.emp_id,
			'emp_app_detail':emp_app_detail_ins,
			'location_type':location['location_type'],
			'location_name':location['location_name']
		}

		return render(request, 'userapp/app_approval/spa_access_approval_form.html',context)

	except Exception as e:
		log.exception(e)
		return redirect('index')


def save_spa_access_detail(request,emp_app_detail):
	''' 
	to save SPA detail
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")

		fields = {}
		emp_app_detail_ins = EmpAppDetail.objects.filter(id=emp_app_detail).first()
		app_ins = emp_app_detail_ins.app_id
		emp_ins = emp_app_detail_ins.emp_id

		app_user_name = None

		fields['Sales Manager'] = request.POST.get('sales_manager',None)
		fields['Sales Manager Email'] = request.POST.get('sales_manager_email',None)
		fields['Business Manager'] = request.POST.get('business_manager',None)
		fields['Business Manager Email'] = request.POST.get('business_manager_email',None)
		fields['Division'] = request.POST.get('division',None)
		ticket_no = request.POST.get('ticket_no',None)

		emp_app_detail_ins.app_login=app_user_name
		emp_app_detail_ins.emp_app_status=ACTIVE

		if ticket_no:
			emp_app_detail_ins.ticket_no=ticket_no

		emp_app_detail_ins.save()

		for key,value in fields.items():

			field_obj = AppFieldValue()    
			field_obj.app_id = app_ins
			field_obj.emp_id = emp_ins
			field_obj.field_name = key
			field_obj.field_value = value
			field_obj.save()

		dsp_ins=SPAApp(emp_ins.id,app_ins.id)
		dsp_ins.app_approval_status(level=2,status='APPROVED')
		dsp_ins.approval_3()

		return render(request, 'userapp/thank_you.html')

	except Exception as e:
		log.exception(e)
		return render(request, 'userapp/page_500.html')


def app_info_holder(request,emp_app_detail):
	'''
	to get app info holder detail
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		if emp_app_detail:
			emp_app_detail_ins = EmpAppDetail.objects.filter(id=emp_app_detail).first()
			print(emp_app_detail_ins.id)
			master_table_id=emp_app_detail_ins.emp_id.master_table_id
			master_table_type=emp_app_detail_ins.emp_id.master_table_type
			mater_table=LocationCl(master_table_id,master_table_type)
			location = mater_table.getLocation()

			context = {
			'emp_app_detail':emp_app_detail_ins,
			'emp':emp_app_detail_ins.emp_id,
			'location_type':location['location_type'],
			'location_name':location['location_name']
			}

			return render(request,'userapp/app_approval/app_info_holder.html',context)
	except Exception as e:
		log.exception(e)
		return redirect('index')	

######################################## EDIT PROCESS################################################

@login_required
def edit_employee(request,emp_code):
	"""
		For updating basic details of employee
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")

		emp = EmployeeMaster.objects.get(emp_code = emp_code)

		if request.method=='GET':
			"""
				To pass data for edit_employee view
			"""
			edit = request.GET.get('ed',False)
			if edit and edit=='True':
				emp = EmployeeMaster.objects.get(emp_code = emp_code)
				log.info('emp',emp)
				apps = AppMaster.objects.all()
				
				app_details = {}

				for app in apps:
					emp_app_details = EmpAppDetail.objects.filter(emp_id=emp.id, app_id=app.id)
					if emp_app_details.exists():
						for emp_app_detail in emp_app_details:
							if emp_app_detail:
								app_details[app.app_name] = emp_app_detail.emp_app_status
					else:
						app_details[app.app_name] = 'Inactive'	

				vertical_list = VerticalMaster.objects.all()
				region_list = RegionMaster.objects.all()
				division_list = DivisionMaster.objects.all()
				branch_list = BranchMaster.objects.all()
				country_list = CountryMaster.objects.all()

				emp_master_id = emp.master_table_id
				master_table_type = emp.master_table_type

				vertical_id = None
				region_id = None
				division_id = None
				branch_id = None

				if master_table_type=='VERTICAL':
					vertical_id = VerticalMaster.objects.filter(id=emp_master_id).first()

				if master_table_type=='REGION':
					region_id = RegionMaster.objects.filter(id=emp_master_id).first()
					vertical_id = region_id.vertical_id

				if master_table_type=='DIVISION':
					division_id = DesignationMaster.objects.filter(id=emp_master_id).first()
					region_id = division_id.region_id
					vertical_id = region_id.vertical_id

				if master_table_type=='BRANCH':
					branch_id = BranchMaster.objects.filter(id=emp_master_id).first()
					if branch_id:
						division_id = branch_id.division_id
						if branch_id.vertical_id:
							vertical_id =branch_id.vertical_id
					if division_id:
						region_id = division_id.region_id
					if region_id :
						vertical_id = region_id.vertical_id
				
				designation_list = DesignationMaster.objects.all()
				branch_manager_list = []

				context = {
					'vertical_list':vertical_list,
					'region_list' : region_list,
					'division_list' : division_list,
					'branch_list' : branch_list,
					'emp_master_id':emp_master_id,
					'master_table_type':master_table_type,
					'designation_list' : designation_list,
					'emp': emp,
					'edit':True,
					'app_details':app_details,
					'branch_id' : branch_id,
					'division_id' : division_id,
					'region_id' : region_id,
					'vertical_id' : vertical_id,
					'country_list' : country_list,
					}

				return render(request, 'userapp/employee_edit.html', context)	
	except Exception as e: 
		log.exception(e)
		return redirect('index')


def temp_edit_employee(request,emp_code):
	'''
	to save edit emp detail temporary
	'''
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")

		if request.method=='POST':
			"""
			Updating employee details
			"""
			# Getting data from edit form #
			
			emp_first = request.POST.get('emp_first',None)
			emp_last = request.POST.get('emp_last',None)
			emp_email = request.POST.get('emp_email',None)
			emp_mobile = request.POST.get('emp_mobile',None)
			emp_address = request.POST.get('emp_address',None)
			remark = request.POST.get('remark',None)
			
			vertical = request.POST.getlist('vertical') or None
			division = request.POST.getlist('division') or None
			region = request.POST.getlist('region') or None
			branch = request.POST.getlist('branch') or None
			designation = request.POST.getlist('designation',None) or None

			emp_dob = request.POST.get('emp_dob',None)
			emp_doj = request.POST.get('emp_doj',None)
			emp_status = request.POST.get('emp_status',None)
			emp_country = request.POST.get('country',None)

			emp_authority = request.POST.get('authority',None)
			emp_authority_email = request.POST.get('authority_email',None)
			
			# Parsing date birth and Date of joining #
			emp_dob_str=parse_date(emp_dob)
			emp_doj_str=parse_date(emp_doj)

			emp_obj = EmployeeMaster.objects.filter(emp_code=emp_code).first()
			emp_ins1 = TempEmployeeMaster.objects.filter(emp_code=emp_code).first()

			if emp_ins1 is None:
				emp_ins = TempEmployeeMaster()	
			else:
				emp_ins = emp_ins1

			if vertical :
				if not vertical[0] in [str("None"),""]:
					vertical_ins = VerticalMaster.objects.filter(id=vertical[0]).first()
					if vertical_ins is not None:
						emp_ins.master_table_id = vertical_ins.id
						emp_ins.master_table_type = 'VERTICAL'

			if region :
				if not region[0] in [str("None"),""] :
					region_ins = RegionMaster.objects.filter(id=region[0]).first()
					if region_ins is not None:
						emp_ins.master_table_id = region_ins.id
						emp_ins.master_table_type = 'REGION'

			if division :
				if not division[0] in [str("None"),""]:
					division_ins = DivisionMaster.objects.filter(id=division[0]).first()
					if division_ins is not None:
						emp_ins.master_table_id = division_ins.id
						emp_ins.master_table_type = 'DIVISION'

			if branch :
				if not branch[0] in [str("None"),""]:
					branch_ins = BranchMaster.objects.filter(id = branch[0]).first()
					if branch_ins is not None:
						emp_ins.master_table_id = branch_ins.id
						emp_ins.master_table_type = 'BRANCH'

			if designation :

				if not designation[0] in [str("None"),""] :
					designation_ins = DesignationMaster.objects.filter(id = designation[0]).first()
					if  designation_ins:
						emp_ins.emp_desg_id = designation_ins.id

			emp_ins.emp_code = emp_code
			emp_ins.emp_fname = emp_first
			emp_ins.emp_lname = emp_last
			emp_ins.emp_email=emp_email
			emp_ins.emp_mobile=emp_mobile 
			emp_ins.emp_address=emp_address 
			emp_ins.remark=remark 

			emp_ins.reporting_authority=emp_authority 
			emp_ins.reporting_authority_email=emp_authority_email 

			country_obj = CountryMaster.objects.filter(id = emp_country).first()

			emp_ins.country = country_obj
			emp_ins.country_isd_code = country_obj.country_isd_code

			emp_ins.emp_status=emp_status  
			emp_ins.date_of_joining=emp_doj_str
			emp_ins.emp_dob = emp_dob_str
			emp_ins.save()

			real_emp_ins = EmployeeMaster.objects.get(emp_code=emp_code)

			to_mail = real_emp_ins.reporting_authority_email

			edit_mail_to_bm(request,emp_ins,to_mail)

			emp_obj.edit = 'Requested'
			emp_obj.save()

			# log for emp update request action
			log_obj = AppLogCl(real_emp_ins.id)
			action="Employee data update Request"
			action_by = request.user.username
			log_obj.create_log(action,action_by)

			return redirect ('employee_detail',emp_code=emp_code)
		else:
			pass

	except Exception as e:
		log.exception(e)


def edit_employee_approval(request, emp_code):
	"""
	to send employee edit details to manager to approve/reject request
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp = TempEmployeeMaster.objects.get(emp_code = emp_code)

		location_type = emp.master_table_type

		if location_type == 'VERTICAL':
			location = VerticalMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type == 'REGION':
			location = RegionMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type == 'DIVISION':
			location = DivisionMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type =='BRANCH':
			location = BranchMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		
		designation_list = DesignationMaster.objects.all()
		branch_manager_list = []

		context = {
				'emp': emp,
				'location_type':location_type,
				'location':location,
				}
		return render(request, 'userapp/edit_employee_approval_form.html', context)

	except Exception as e: 
		log.exception(e)
		return redirect('index')		


def reject_employee_edit(request):
	"""
	to send reject employee email to service now and update emp status
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		if request.method == 'POST':

			emp_code = request.POST['emp_code']
			reason = request.POST['reason']

			emp_obj = EmployeeMaster.objects.get(emp_code=emp_code)

			TempEmployeeMaster.objects.filter(emp_code=emp_code).update(emp_status='Rejected', rejection_reason=reason)

			msub="Employee Edit Approval {} {} got rejected".format(emp_obj.emp_fname, emp_obj.emp_lname)
			mbody="Employee Details : {}, {}, {}  is rejected by Branch Manager {}. Reason: {}.".format(emp_obj.emp_code,emp_obj.emp_fname,emp_obj.emp_desg.desg_name, emp_obj.reporting_authority,reason)
			mto = 'priya.gupta@rentokil-pci.com'
			mfrom=SYSMAIL
			app_task(args=(msub,mbody,mfrom,mto))

			emp_obj.edit = 'Rejected'
			emp_obj.save()

			# log for Edit Rejected action
			log_obj = AppLogCl(emp_obj.id)
			action="Employee data update Request Rejected"
			action_by = request.user.username
			log_obj.create_log(action,action_by)

		else :
			pass	

		return render(request, 'userapp/thank_you.html')

	except Exception as e: 
		log.exception(e)
		return redirect('index')		


def approve_employee_edit(request):
	"""
	to send approve employee email to service now and update emp status
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")

		if request.method == 'POST':

			emp_code = request.POST.get('emp_code')
			
			real_emp_ins = EmployeeMaster.objects.get(emp_code = emp_code)
			temp_emp_ins = TempEmployeeMaster.objects.get(emp_code = emp_code)

			real_emp_ins.emp_fname = temp_emp_ins.emp_fname
			real_emp_ins.emp_lname = temp_emp_ins.emp_lname
			real_emp_ins.emp_email = temp_emp_ins.emp_email
			real_emp_ins.emp_address = temp_emp_ins.emp_address
			real_emp_ins.emp_mobile = temp_emp_ins.emp_mobile
			real_emp_ins.reporting_authority = temp_emp_ins.reporting_authority
			real_emp_ins.emp_reporting_authority_email = temp_emp_ins.reporting_authority_email
			real_emp_ins.country = temp_emp_ins.country
			real_emp_ins.country_isd_code = temp_emp_ins.country_isd_code
			real_emp_ins.date_of_joining = temp_emp_ins.date_of_joining
			real_emp_ins.emp_dob = temp_emp_ins.emp_dob
			real_emp_ins.master_table_id = temp_emp_ins.master_table_id
			real_emp_ins.master_table_type = temp_emp_ins.master_table_type
			real_emp_ins.emp_desg = temp_emp_ins.emp_desg
			real_emp_ins.edit = 'Approved'
			real_emp_ins.save()
			TempEmployeeMaster.objects.filter(emp_code=emp_code).update(emp_status='Approved')

			msub="Employee Edit Approval {} {} got Approved".format(real_emp_ins.emp_fname, real_emp_ins.emp_lname)
			mbody="Employee Details : {}, {}, {}  is Approved by Branch Manager {}.".format(real_emp_ins.emp_code,real_emp_ins.emp_fname,real_emp_ins.emp_desg.desg_name, real_emp_ins.reporting_authority)
			mto = 'priya.gupta@rentokil-pci.com'
			mfrom=SYSMAIL
			app_task(args=(msub,mbody,mfrom,mto))

			# log for Emp edit Approve action
			log_obj = AppLogCl(real_emp_ins.id)
			action="Employee data update Request Approved"
			action_by = request.user.username
			log_obj.create_log(action,action_by)

		else :
			pass	

		return render(request, 'userapp/thank_you.html')

	except Exception as e: 
		log.exception(e)
		return redirect('index')		


############## Deactivate/Activate Employee ######################################################


@login_required
def active_deactive_employee(request,emp_code,action_taken):
	"""
	Activate/Deactivate employee
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")

		if request.method == 'GET':
			log.info('entering get method')
			log.info("%s" % (str(action_taken)))
			
			emp_ins = EmployeeMaster.objects.get(emp_code=emp_code)

			if action_taken == 'deactivate':
				emp_ins.deactivate = 'Requested'
				emp_ins.save()

			else:
				emp_ins.activate = 'Requested'
				emp_ins.save()	

			log.info("sending mail")
			msub="Employee {action_taken} approval mail for Employee Code: {emp_code}".format(action_taken=action_taken,emp_code=emp_code )
			mto= 'priya.gupta@rentokil-pci.com'
			mfrom=SYSMAIL
			host = request.get_host()
			url = "http://{host}/active_deactive_employee_approval/{ecode}/{action_taken}/".format(host=host,ecode=emp_ins.emp_code,action_taken=action_taken)
			mbody="Please click on below link to Approve/Disapprove Employee {action_taken} Request. Detail: {url}.".format(action_taken= action_taken,url=url)
		  
			app_task(args=(msub,mbody,mfrom,mto))
			log.info("sent")	

			# log for employee active/deactive request
			log_obj = AppLogCl(emp_ins.id)
			action="Employee {action_taken} Requested".format(action_taken=action_taken)
			action_by = request.user.username
			log_obj.create_log(action,action_by)

			log.info('after creating log')

			return employee_detail(request, emp_code)
		else:
			pass

	except Exception as e: 
		log.exception(e)
		return redirect('index')


def active_deactive_employee_approval(request, emp_code, action_taken):
	"""
	to send employee details to HR to approve/reject employee activate/deactivate request
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		emp = EmployeeMaster.objects.get(emp_code = emp_code)

		location_type = emp.master_table_type

		if location_type == 'VERTICAL':
			location = VerticalMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type == 'REGION':
			location = RegionMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type == 'DIVISION':
			location = DivisionMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		elif location_type =='BRANCH':
			location = BranchMaster.objects.get(id = emp.master_table_id)
			manager = location.manager_name
		
		designation_list = DesignationMaster.objects.all()
		branch_manager_list = []

		context = {
				'emp': emp,
				'location_type':location_type,
				'location':location,
				'action_taken':action_taken,
				}

		return render(request, 'userapp/active_deactive_employee_approval_form.html', context)

	except Exception as e: 
		log.exception(e)
		return redirect('index')	


@login_required
def approve_active_deactive_employee(request,action_taken):
	"""
	approve
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		if request.method == 'POST':

			emp_code = request.POST.get('emp_code')
			emp_ins = EmployeeMaster.objects.get(emp_code=emp_code)

			if action_taken == 'deactivate':
				
				emp_ins.active = False
				emp_ins.emp_status = 'Inactive'
				emp_ins.deactivate = 'Approved'
				emp_ins.save()

			else:
				emp_ins.active = True
				emp_ins.emp_status = 'Active'
				emp_ins.activate = 'Approved'
				emp_ins.save()

			msub="Employee {} Approval {} {} got Approved".format(action_taken,emp_ins.emp_fname, emp_ins.emp_lname)
			mbody="Employee Details : {}, {}, {}  is Approved by HR.".format(emp_ins.emp_code, emp_ins.emp_fname, emp_ins.emp_desg.desg_name)
			mto = 'priya.gupta@rentokil-pci.com'
			mfrom=SYSMAIL
			app_task(args=(msub,mbody,mfrom,mto))	

			# log for appove active/deactive emp
			log_obj = AppLogCl(emp_ins.id)
			action="Employee {action_taken} Approved".format(action_taken=action_taken)
			action_by = request.user.username
			log_obj.create_log(action,action_by)

		else:
			pass
		return render(request, 'userapp/confirm.html', {'msg':'Email has been dent to Helpdesk'})		
	except Exception as e: 
		log.exception(e)
		return redirect('index')	


@login_required
def reject_active_deactive_employee(request,action_taken):
	"""
	Activate employee 
	"""
	log.debug("Entering %s method" % (whoami()))  
	try:
		log.info("Entering try block")
		if request.method == 'POST':

			emp_code = request.POST.get('emp_code')
			emp_ins = EmployeeMaster.objects.get(emp_code=emp_code)
			reason = request.POST.get('reason')

			if action_taken == 'deactivate':		
				emp_ins.deactivate = 'Rejected'
				emp_ins.save()

			else:
				emp_ins.activate = 'Rejected'
				emp_ins.save()

			msub="Employee {} Approval {} {} got Rejected".format(action_taken,emp_ins.emp_fname, emp_ins.emp_lname)
			mbody="Employee Details : {}, {}, {}  is Rejected by HR. Reason: {}.".format(emp_ins.emp_code,emp_ins.emp_fname,emp_ins.emp_desg.desg_name,reason)
			mto = 'priya.gupta@rentokil-pci.com'
			mfrom=SYSMAIL
			app_task(args=(msub,mbody,mfrom,mto))	

			# log for emp active/deactive rejected action
			log_obj = AppLogCl(emp_ins.id)
			action="Employee {action_taken} Rejected".format(action_taken=action_taken)
			action_by = request.user.username
			log_obj.create_log(action,action_by)
		else:
			pass	
		return render(request, 'userapp/confirm.html', {'msg':'Email has been dent to Helpdesk'})	

	except Exception as e: 
		log.exception(e)
		return redirect('index')