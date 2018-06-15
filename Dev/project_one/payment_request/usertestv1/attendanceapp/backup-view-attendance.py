import re
import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from userapp.util import mail_to_bm, app_task, leave_app_mail, leave_mail_approved
from userapp.models import EmployeeMaster, DesignationMaster, BranchMaster, DivisionMaster
from .models import LeaveMaster,CoverageMaster,LeaveTypesMaster,StateName,HolidayListMaster,HolidayTypeMaster
from datetime import date, timedelta

# Create your views here.

def leave_index(request):
	"""
	to show all employee records
	"""
	print("====I M IN LEAVE INDEX====")
	emp_br = ''
	date_from = ''
	date_till = ''
	dates = []
	dic = {}
	# dic_date = {}
	atdn_list =[] 
	date_list =[]
	date_1 = datetime.date.today
	lv_date_from = datetime.date.today
	lv_date_to = datetime.date.today
	try:
		emps = EmployeeMaster.objects.all()
		leavemaster = LeaveMaster.objects.all()
		lev_typ = LeaveTypesMaster.objects.all()
		
		if request.method == 'POST':

			"""
			Search function for employee list view employee code,branch and status
			"""
			emp_br = request.POST.getlist('leave_branch',False)
			print('-----emp_br----',emp_br)
			date_from = request.POST.get('date_from',False)
			date_till = request.POST.get('date_to',False)
			name =''
			d1 = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()            # From date of Attendance Report
			d2 = datetime.datetime.strptime(date_till, '%Y-%m-%d').date()            # Till date of Attendance Report
			delta = d2 - d1   
			print('-----delta----',delta)                                           # timedelta
			if emp_br :
				if emp_br[0]!="":                                                      #Check if branch is selected in Attendance report
					
					emps_br_filter = emps.filter(master_table_type='BRANCH')             #Get all Employees Of Selected Branch
					print('-----emps_br_filter----',emps_br_filter)
					if emps_br_filter: 
						emps_br_filter_2 = emps.filter(master_table_id=emp_br[0])
						if emps_br_filter_2:

							#Get all Employees Of Selected Branch

							if emps_br_filter_2 != None :
								
								for emp in emps_br_filter_2:
									name = emp.emp_fname + emp.emp_lname
									leaves = leavemaster.filter(emp_id = emp)                     #Check if Employee has taken any leave in between selected date range
									print('-----leaves----',leaves)
									if len(leaves) > 0:
										for i in range(delta.days + 1):                             #Loop to get Date 1 by 1 which is btw From Date and Till Date Selected by User
											date_1 = d1 + timedelta(days=i)
											# print('--------date searched----',date_1)
											dates.append(date_1)
											day = date_1.weekday()                                     # To find Sunday's Eg: if day = 0 then the day is Monday similarly in variable day = 6 then the day is Sunday
											print('------day-----',day)
											for leave in leaves:
												lv_date_from = leave.date_from.date()                     #Employee from date leave
												lv_date_to = leave.date_to.date()                         #Employee to date leave
												delta_2 = lv_date_to - lv_date_from   
												for lev_date in range(delta_2.days + 1):                  # loop to check if current leave date is equal to current(Date in between the provided date range) date
													print('==**********',lev_date)
													date_lev = lv_date_from + timedelta(days=lev_date)
													if day == 6:
														value = 'WeekOff'												
													elif date_lev == date_1:                                  # Comparing if leave from date is equal to current (date selected in attendance report)date
														value = leave.leave_type_id.leave_type
													else:
														value = 'Present'
												date_list.append(value)
										dic = {'emp_code':emp.emp_code,'emp_name':name,'dates':date_list}
										atdn_list.append(dic)

						print("====atdn_list=========",atdn_list)
		else:
			leaves = LeaveMaster.objects.all()
		# depart_list = DepartmentMaster.objects.all()
		desgn_list = DesignationMaster.objects.all()
		div_list = DivisionMaster.objects.all()
		branch_list = BranchMaster.objects.all()
		
		return render(request, 'userapp/leave_list.html', {'branch_list':branch_list,'dates':dates,'atdn_list':atdn_list,'leave_branch':emp_br,'date_from':date_from,'date_to':date_till})

	except Exception as e: 
		print("=============================Exception :",e)
		return render(request, 'userapp/page_404.html')


def export_to_csv(request, leave_branch, date_from, date_to):
	"""
	Export To CSV File Function
	"""
	dates = []
	dic = {}
	atdn_list =[] 
	date_list =[]
	date_1 = datetime.date.today
	lv_date_from = datetime.date.today
	lv_date_to = datetime.date.today
	try:
		emps = EmployeeMaster.objects.all()
		leavemaster = LeaveMaster.objects.all()
		lev_typ = LeaveTypesMaster.objects.all()
		
		# if request.method == 'POST':

		"""
		Search function for employee list view employee code,branch and status
		"""
		emp_br = leave_branch
		print('-----emp_br----',emp_br)
		date_from = date_from
		date_till = date_to
		name =''
		d1 = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()            # From date of Attendance Report
		d2 = datetime.datetime.strptime(date_till, '%Y-%m-%d').date()            # Till date of Attendance Report
		delta = d2 - d1   
		print('-----delta----',delta)                                           # timedelta
		if emp_br :
			if emp_br[0]!="":                                                      #Check if branch is selected in Attendance report
				
				emps_br_filter = emps.filter(master_table_type='BRANCH')             #Get all Employees Of Selected Branch
				print('-----emps_br_filter----',emps_br_filter)
				if emps_br_filter: 
					emps_br_filter_2 = emps.filter(master_table_id=emp_br[0])
					if emps_br_filter_2:

						#Get all Employees Of Selected Branch

						if emps_br_filter_2 != None :
							
							for emp in emps_br_filter_2:
								name = emp.emp_fname + emp.emp_lname
								leaves = leavemaster.filter(emp_id = emp)                     #Check if Employee has taken any leave in between selected date range
								print('-----leaves----',leaves)
								if len(leaves) > 0:
									for i in range(delta.days + 1):                             #Loop to get Date 1 by 1 which is btw From Date and Till Date Selected by User
										date_1 = d1 + timedelta(days=i)
										dates.append(date_1)
										day = date_1.weekday()                                     # To find Sunday's Eg: if day = 0 then the day is Monday similarly in variable day = 6 then the day is Sunday
										for leave in leaves:
											lv_date_from = leave.date_from.date()                     #Employee from date leave
											lv_date_to = leave.date_to.date()                         #Employee to date leave
											delta_2 = lv_date_to - lv_date_from   
											for lev_date in range(delta_2.days + 1):                  # loop to check if current leave date is equal to current(Date in between the provided date range) date
												date_lev = lv_date_from + timedelta(days=lev_date)
												if day == 6:
													value = 'WeekOff'												
												elif date_lev == date_1:                                  # Comparing if leave from date is equal to current (date selected in attendance report)date
													value = leave.leave_type_id.leave_type
												else:
													value = 'Present'
											date_list.append(value)
									dic = {'emp_code':emp.emp_code,'emp_name':name,'dates':date_list}
									atdn_list.append(dic)

					print("====atdn_list=========",atdn_list)
	# else:
		# leaves = LeaveMaster.objects.all()
		# depart_list = DepartmentMaster.objects.all()
		# desgn_list = DesignationMaster.objects.all()
		# div_list = DivisionMaster.objects.all()
		branch_list = BranchMaster.objects.all()
		
		return render(request, 'userapp/leave_list.html', {'branch_list':branch_list,'dates':dates,'atdn_list':atdn_list})

	except Exception as e: 
		print("=============================Exception :",e)
		return render(request, 'userapp/page_404.html')



# def leave_index(request):
# 	"""
# 	to show all employee records
# 	"""
# 	print("====I M IN LEAVE INDEX====")
# 	dates = []
# 	dic = {}
# 	dic_date = {}
# 	atdn_list =[] 
# 	date_list =[]
# 	date_1 = datetime.date.today
# 	lv_date_from = datetime.date.today
# 	lv_date_to = datetime.date.today
# 	try:
# 		emps = EmployeeMaster.objects.all()
# 		leavemaster = LeaveMaster.objects.all()
# 		lev_typ = LeaveTypesMaster.objects.all()
		
# 		if request.method == 'POST':
# 			"""
# 			Search function for employee list view employee code,branch and status
# 			"""
# 			emp_br = request.POST.getlist('leave_branch',False)
# 			date_from = request.POST.get('date_from',False)
# 			date_till = request.POST.get('date_to',False)
# 			name =''
# 			d1 = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()            # From date of Attendance Report
# 			d2 = datetime.datetime.strptime(date_till, '%Y-%m-%d').date()            # Till date of Attendance Report
# 			delta = d2 - d1                                              # timedelta
# 			if emp_br :
# 				if emp_br[0]!="":                                                      #Check if branch is selected in Attendance report
					
# 					emps_br_filter = emps.filter(master_table_type='BRANCH')             #Get all Employees Of Selected Branch
# 					if emps_br_filter: 
# 						emps_br_filter_2 = emps.filter(master_table_id=emp_br[0])
# 						if emps_br_filter_2:

# 							#Get all Employees Of Selected Branch

# 							if emps_br_filter_2 != None :
								
# 								for emp in emps_br_filter_2:
# 									name = emp.emp_fname + emp.emp_lname
# 									leaves = leavemaster.filter(emp_id = emp)                     #Check if Employee has taken any leave in between selected date range
									
# 									if len(leaves) > 0:
# 										for i in range(delta.days + 1):                             #Loop to get Date 1 by 1 which is btw From Date and Till Date Selected by User
# 											date_1 = d1 + timedelta(days=i)
# 											print('--------date searched----',date_1)
# 											dates.append(date_1)
# 											day = date_1.weekday()
# 											for leave in leaves:
# 												lv_date_from = leave.date_from.date()                     #Employee from date leave
# 												lv_date_to = leave.date_to.date()                         #Employee to date leave
# 												delta_2 = lv_date_to - lv_date_from                       #Difference
# 												for lev_date in range(delta_2.days + 1):                  # loop to check if current leave date is equal to current(Date in between the provided date range) date
# 													print('==**********')
# 													date_lev = lv_date_from + timedelta(days=lev_date)
# 													if date_lev == date_1:                                  # Comparing if leave from date is equal to current (date selected in attendance report)date
# 														print('@@@@@@@@@@',date_lev)
# 														# dic_date[str(date_1)] = leave.leave_type_id.leave_type
# 														date_list.append(leave.leave_type_id.leave_type)
# 													else:
# 														print('#########',date_lev)
# 														# dic_date[str(date_1)] = 'Present'
# 														date_list.append('Present')
# 										# date_list.append(dic_date)
# 										dic = {'emp_code':emp.emp_code,'emp_name':name,'dates':date_list}
# 										atdn_list.append(dic)

# 						print("====atdn_list=========",atdn_list)
# 		else:
# 			leaves = LeaveMaster.objects.all()
# 		# depart_list = DepartmentMaster.objects.all()
# 		desgn_list = DesignationMaster.objects.all()
# 		div_list = DivisionMaster.objects.all()
# 		branch_list = BranchMaster.objects.all()
		
# 		return render(request, 'userapp/leave_list.html', {'branch_list':branch_list,'dates':dates,'atdn_list':atdn_list})

# 	except Exception as e: 
# 		print("=============================Exception :",e)
# 		return render(request, 'userapp/page_404.html')


def leave_application(request):
	"""
	to send employee details to app admin to create app account
	"""
	try:
		emps = EmployeeMaster.objects.all()
		leaves = LeaveTypesMaster.objects.all()

		return render(request, 'userapp/leave_application_form.html',{'emps':emps,'leaves':leaves})
		# return render(request, 'userapp/form.html')
	except Exception as e: 
		print("=*****************Exception :",e)
		return redirect('index')



def add_holiday(request):
	"""
	To Add Holiday List According to State
	"""
	try:
		states = StateName.objects.all()
		holidays = HolidayListMaster.objects.all()
		holiday_type = HolidayTypeMaster.objects.all()
		coverages = CoverageMaster.objects.all()
		# leaves = LeaveMaster.objects.all()
		

		return render(request, 'userapp/add_holiday.html',{'coverages':coverages,'states':states,'holidays':holidays,'holiday_type':holiday_type})
	except Exception as e: 
		print("*****************Exception :",e)
		return redirect('leave_index')

def add_holiday_type(request):
	"""
	To Add Holiday Type 
	"""
	try:
		# states = StateName.objects.all()
		holiday_type = HolidayTypeMaster.objects.all()

		return render(request, 'userapp/add_holiday_type.html',{'holiday_type':holiday_type})
	except Exception as e: 
		print("*****************Exception :",e)
		return redirect('leave_index')



def submit_holiday_type(request):
	"""
	To Submit Holiday Type in Database
	"""
	try:
		if request.method=='POST':
			holiday_type = HolidayTypeMaster()
			hol_type = request.POST.get('hol_type',None)
			print("*****************hol_type :",hol_type)
			if hol_type is not None:
				holiday_type.holiday_type = hol_type
			print("*****************holiday_type.holiday_type :",holiday_type.holiday_type)
			
			holiday_type.save()

			msg = 'Holiday Type added Successfully !!!'
			return render(request, 'userapp/thank_you.html',{'msg':msg})
	except Exception as e: 
		print("*****************Exception :",e)
		return redirect('leave_index')

def submit_new_holiday(request):
	"""
	To Add New Holiday for Selected State in Database
	"""
	try:
		if request.method=='POST':
			states = StateName.objects.all()
			holidays = HolidayListMaster()

			hol_name = request.POST.get('hol_name',False)
			hol_date = request.POST.get('hol_date',None)
			hol_day = request.POST.get('hol_day',False)
			region = request.POST.get('region',False)
			coverage = request.POST.get('coverage',False)
			assigned_by = request.POST.get('assigned_by',False)
			# fix_hol_date = request.POST.get('hol_date')
			# opt_hol_date = request.POST.get('opt_hol_date')
			state = request.POST.getlist('state',False)
			state_ins = StateName.objects.get(id = state[0])

			holiday_type = request.POST.getlist('holiday_type',False)
			print("====holiday_type",holiday_type[0])
			holiday_type_ins = HolidayTypeMaster.objects.get(id = holiday_type[0])

			holidays.holiday_name = hol_name
			holidays.holiday_date = hol_date
			holidays.holiday_day = hol_day
			holidays.leave_type_id = holiday_type_ins
			holidays.coverage = coverage
			holidays.region = region
			holidays.assigned_by = assigned_by
			holidays.state_id=state_ins
			# print("====fix_hol_date",fix_hol_date)
			# print("====opt_hol_date",opt_hol_date)
			
			# if fix_hol_date is not None:
			# 	print("==222222==fix_hol_date",fix_hol_date)
			# 	holidays.fixed_holiday_date = fix_hol_date
			# 	print("====holidays.fixed_holiday_date",holidays.fixed_holiday_date)
			# if opt_hol_date is not None:
			# 	print("==22222222==opt_hol_date",opt_hol_date)
			# 	holidays.optional_holiday_date=opt_hol_date
			 
			
			holidays.save()
			print("***********sssss******holidays :",holidays)

			msg = 'Holiday Added Successfully in Database!!!'
			return render(request, 'userapp/thank_you.html',{'msg':msg})
	except Exception as e: 
		print("*****************Exception :",e)
		return redirect('leave_index')

def holiday_list_search_view(request):
	"""
	To Direct to List/View Holidays where User can get Holiday list by Selecting State and hitting Search Button
	"""
	try:
		states = StateName.objects.all()
		holidays = HolidayListMaster.objects.all()

		return render(request, 'userapp/holiday_list.html',{'states':states,'holidays':holidays})
	except Exception as e: 
		print("*****************Exception :",e)
		return redirect('leave_index')

def list_holiday_index(request):
	"""
	To List/View Holidays Data for Selected State
	"""
	try:
		states = StateName.objects.all()
		holidays = HolidayListMaster.objects.all()

		return render(request, 'userapp/holiday_list.html',{'states':states,'holidays':holidays})
	except Exception as e: 
		print("*****************Exception :",e)
		return redirect('leave_index')


# def get_emp_details(request,emp_code):
# 	"""
# 	To Get Employee Details when user enter Emp Code in Leave Application Form
# 	"""
# 	print("===I M IN GET EMP DETAILS FOORM===")
# 	print("===emp_code===",emp_code)
# 	try:
# 		emps = EmployeeMaster.objects.all()
# 		leaves = LeaveTypesMaster.objects.all()

# 		return render(request, 'userapp/leave_application_form.html',{'emps':emps,'leaves':leaves})

# 	except Exception as e: 
# 		print("=*****************Exception :",e)
# 		return redirect('index')		

def submit_leave(request):
	"""
	OnClick of Submit button in Leave Application Form, mail will go to respective Reporting manager to approve or disapprove leave request
	"""
	try:
		if request.method == 'POST':
			user_name = request.POST['user_name']
			emp_code = request.POST['emp_code']
			user_email = request.POST['user_email']
			leave_type = request.POST.get('leave_type')

			date_from = request.POST['date_from']
			date_to = request.POST['date_to']

			print('-----date_from---',date_from)
			print('-----date_to---',date_to)

			leave_ins = LeaveMaster()
			# print('-----emp_code---',emp_code)
			emp = EmployeeMaster.objects.get(emp_code = emp_code)

			# print('-----emp---',emp)
			leave_type_ins = LeaveTypesMaster.objects.get(id = leave_type[0])

			leave_ins.emp_code = emp_code
			leave_ins.emp_id = emp
			leave_ins.emp_name = user_name
			leave_ins.user_email = user_email
			leave_ins.leave_type_id = leave_type_ins
			leave_ins.date_from = date_from
			leave_ins.date_to = date_to

			print('-----leave_ins.date_from---',leave_ins.date_from)
			print('-----leave_ins.date_to---',leave_ins.date_to)

			leave_ins.save()
			print('-----leave_ins.date_from---',leave_ins.date_from)
			print('-----leave_ins.date_to---',leave_ins.date_to)
			print('-----leave_ins---',leave_ins)
			ip = 'localhost'
			msub="Leave Approval Request"
			mbody="Please click on below link to Approve/Disapprove Employee Leave Application http://{0}:8000/leave_approval/{1}".format(ip,leave_ins.emp_code)
			# mto = str(emp.emp_manager.bm_email)
			mto='priyanka.chaurasia@rentokil-pci.com'
			print(mto)

			mfrom='omiharjani@gmail.com'
			leave_app_mail(request,leave_ins,mto)

		return render(request, 'userapp/thank_you.html')

	except Exception as e: 
		print("=*****************Exception :",e)
		return redirect('index')	


def leave_approval(request, emp_code, leave_id):
	"""
	to send employee details to manager to approve/reject employee
	"""
	try:
		emp = EmployeeMaster.objects.get(emp_code = emp_code)
		leave = LeaveMaster.objects.get(emp_code = emp_code, id = leave_id)
		return render(request, 'userapp/leave_approval.html', {'leave': leave})

	except Exception as e: 
		print("Exception====&&&&&&&&&&==== :",e)
		return redirect('index')


# def leave_list(request):
# 	"""
# 	List Employee Leave Status 
# 	"""
# 	try:
# 		# emp = EmployeeMaster.objects.all()
# 		leaves = LeaveMaster.objects.all()
# 		print("====leave===kkkkkkkkkk===",leaves)
# 		return render(request, 'userapp/leave_list.html', {'leaves': leaves})

# 	except Exception as e: 
# 		print("Exception :",e)
# 		return redirect('index')

def approved_leave(request,leave_id,leave_emp_code):
	"""
	Function to Send mail to Employee after manager approves its Leave Request
	"""
	try:
		emp = EmployeeMaster.objects.get(emp_code = leave_emp_code)
		leave = LeaveMaster.objects.get(emp_code = leave_emp_code, id = leave_id)
		if leave:
			leave.leave_status = 'Approved'
			leave.save()
		ip = 'localhost'
		msub="Leave Request Approved"
		mbody="Dear Employee,&nbsp;This mail is to inform you that,Your Leave Request is Approved by Manager"
		mto = str(emp.emp_manager.bm_email)
		print(mto)

		mfrom='omiharjani@gmail.com'
		leave_mail_approved(request,leave,mto)

		return render(request, 'userapp/thank_you.html')

	except Exception as e: 
		print("Exception======:",e)
		return redirect('index')


def reject_leave(request,leave_id,leave_emp_code):
	print("===U R IN REJECT LEAVE")
	"""
	to send reject employee email to service now and update emp status
	"""
	try:
		if request.method == 'POST':

			emp_code = request.POST['emp_code']
			reason = request.POST['reason']
			leave_id = leave_id
			# emp = EmployeeMaster.objects.get(emp_code = leave_emp_code)
			leave = LeaveMaster.objects.get(emp_code = leave_emp_code, id = 28)
			if leave:
				leave.leave_status = 'Rejected'
				leave.save()
			print("-------------",leave.leave_status)
			msub="Employee {} got rejected".format(leave.emp_name)
			mbody="This mail is to inform that Employee : {}, is rejected by Branch Manager {}. Reason: {}.".format(leave.emp_name,leave.emp_id.emp_manager.bm_name,reason)

			mto = "omiharjani@gmail.com"

			mfrom='omiharjani@gmail.com'
			app_task(args=(msub,mbody,mfrom,mto))
		else :
			pass	

		return render(request, 'userapp/thank_you.html')

	except Exception as e: 
		print("Exception :",e)
		return redirect('index')	
