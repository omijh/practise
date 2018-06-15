from django.core.mail import send_mail, EmailMultiAlternatives
import threading
from .constant import *
from .models import EmployeeMaster,BranchMaster,DivisionMaster,DesignationMaster,AppMaster,EmpAppDetail,AppRole,AppAdmin,VerticalMaster,RegionMaster,RequestId,CountryMaster,AppApprovalLog,AppLog,AppApproverMaster,AppApprovalStatus

# Leave Application 

def leave_app_mail(request,leave_ins,mto):
	"""
	    Mail to BranchManager/HeadOfDepartment with application link and security code to approve/Disapprove Employee Leave Request
	"""
	print("sending mail")
	ip = HOST
	host = HOST
	url = "http://{host}/leave_approval/{ecode}/{leave_id}".format(host=host,ecode=leave_ins.emp_code,leave_id=leave_ins.id)
	msub = "Leave Approval Request"
	mto = mto
	mfrom=SYSMAIL
	# subject, from_email, to = 'hello', 'priyanka.chaurasia158@gmail.com', 'priyanka.chaurasia@rentokil-pci.com'
	# text_content = 'This is an important message.'
	mbody = """<html><body>
	<p>Hello,</p>
	<p>Following is the Employee Details who has Requested for Leave Approval</p>
	<br>
	<p>Employee Code :""" + leave_ins.emp_code + """</p>
	<p>Employee Name :""" + leave_ins.emp_name + """</p>

	<h3><p>Please click on below link to Approve/Disapprove Employee Leave Application.</p></h3>
	""" + url  + """
	<p>Thanks!!</p>
	</body></html>"""
	app_task(args=(msub,mbody,mfrom,mto))
	print("=====mail sent=======")
	return True


def leave_mail_approved(request,leave_ins,mto):
    print("====U R IN LEAVE MAIL APPROVED====")
    """
        Mail to BranchManager/HeadOfDepartment with application link and security code to approve/Disapprove Employee Leave Request
    """
    print("sending mail")
    # host = request.get_host()
    # ip = 'localhost'
    msub="Leave Request Approved By Branch Manager"
    # mbody="Dear Employee,This mail is to inform you that,Your Leave Request is Approved by Manager"

    mbody = """<html><body>
    <p>Dear""" + leave_ins.emp_name + """,</p>
    <p>This mail is to inform you that,Your Leave Request has been Approved by Manager</p>
    <br>
    <p>Thanks!!</p>
    </body></html>"""

    mfrom=SYSMAIL
    mto = mto
  
    app_task(args=(msub,mbody,mfrom,mto))
    return True 


def mail_to_bm(request,emp_ins,to_mail):
	"""
		Mail to branch manager with application link and security code to approve/Disapprove employee
	"""

	print("sending mail")
	msub="Employee approve mail"
	# mto = str(emp_ins.emp_manager.bm_email)
	mto=to_mail
	mfrom=SYSMAIL
	host = request.get_host()

	# scode = SecurityCode.objects.get(emp_code=emp_ins)

	url = "http://{host}/employee_approval/{ecode}/".format(host=host,ecode=emp_ins.emp_code)
	
	# mbody="Please click on below link to Approve/Disapprove Employee & provide Application Access Rights {url}. Security code : {scode}".format(url=url,scode=scode.code)

	mbody="Please click on below link to Approve/Disapprove Employee & provide Application Access Rights {url}.".format(url=url)
  
	app_task(args=(msub,mbody,mfrom,mto))
	print("sent")
	return True

def app_send_mail(msub,mbody,mfrom,mto):
  print("Sending mail...................{0}".format(mto))
  text_content = 'This is an important message.'
  msg = EmailMultiAlternatives(msub, text_content, mfrom, [mto])
  msg.attach_alternative(mbody, "text/html")
  msg.send()
  return True

# def app_send_mail(msub,mbody,mfrom,mto):

# 	print("Sending mail...................{0}".format(mto))
# 	send_mail(msub,mbody,mfrom,[mto],fail_silently=False,)
# 	return True


def app_task(args,target=app_send_mail):
	"""
	To send mail th
	"""

	t = threading.Thread(target=target, args=args, kwargs={})
	t.setDaemon(True)
	t.start()


def mail_to_service_now(request,to_mail,mbody):
   """
	   Mail to Service Now to Acknowledge Application Account Created.
   """
   print("sending mail========")
   msub="Application Account Activation"
   mto=to_mail
   mfrom=SYSMAIL
   host = request.get_host()

   mbody=mbody
 
   app_task(args=(msub,mbody,mfrom,mto))
   print("sent mail to Service Now******************")
   return True    

# new changes by selvam #

class GmailApp:

	def __init__(self,emp_id,app_id):
		self.emp_id = emp_id
		self.app_id = app_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()
		self.app_ins=AppMaster.objects.filter(id=app_id).first()
		self.empapp_detail_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()

		# self.sn_mail = SYSMAIL

		# self.app_info_mail = SYSMAIL


	def approval_1(self):
		approval_level='1'

		sn = self.mail_to_sn(action=approval_level)
		if sn:
			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()

			print('EMP APP DEATIL ......ADMIN....INPROGRESS')

			return True
		else:
			return False
		


	def approval_2(self):

		approval_level='2'
		print("In create account.............")
		sn = self.mail_to_sn(action=approval_level)

		if sn:
			print('EMP APP DEATIL ......GAMIL....INPROGRESS')
			return True
		else:
			return False
	

	def approval_3(self):

		approval_level='3'

		if self.empapp_detail_ins.emp_app_status == ACTIVE:

			# self.add_app_approval_log(ACC_CREATED,self.sn_mail,mto=None,mail_status=True)
			sn=self.mail_to_sn(approval_level)

			if sn:
				return True
			else :
				return False

			# self.add_app_approval_log(ACC_CREDENT_SEND,SYSTEM,mto=self.sn_mail,mail_status=True)
		
		else:
			return False

	def check_bm_approval(self):
		emp_app_detail = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
		print("Check bm approval.......................")
		if emp_app_detail:
			if emp_app_detail.emp_app_status in [ACKL]:
				return True
			return False
		else:
			return False

		
	def mail_to_sn(self,action=None):

		ip=HOST
		approval_level=action

		if approval_level=='1':
			
			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)
				# rrrrrrrrrr
				url = "http://{}/admin_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=self.empapp_detail_ins.id)

				msub="{0} app access rights for Employee code:{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)
				
				mbody="Please click on below link to Approve {0} application access rights for Employee http://{1}/app_info_holder/{2}/".format(self.app_ins.app_name,HOST,self.empapp_detail_ins.id)

				mto = app_appr_master.approver_email
				# mto = SYSMAIL
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))

				return True
			else:
				return False
		

		elif approval_level=='2':
 
			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()
			if app_appr_master:
				print("Sending mail to ..............sn")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				url = "http://{}/emp_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee app detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,emp_app_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)

				mto = app_appr_master.approver_email    # mail goes to Service Now
				# mto = SYSMAIL
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				return False


		elif approval_level=='3':

			#add_app_approval_log('APPROVAL_1_APPROVED',,mto=None,mail_status=True)

			ip = HOST

			msub="{0} account created for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

			mbody="This is to inform you that  Account for Application :{0} has been Activated with User Name :{1} & Password : {2}".format(self.app_ins.app_name,self.empapp_detail_ins.app_login,self.empapp_detail_ins.app_pass)

			log_obj = AppLogCl(self.emp_ins.id)
			action="{} Account Created".format(self.app_ins.app_name)
			action_by ="Service Now"
			log_obj.create_log(action,action_by)

			# mto =self.sn_mail
			mto =self.emp_ins.reporting_authority_email   # mail goes to Reporting Authority
			mfrom = ''
			# to_mail = SYSMAIL
			# mail_to_service_now(None,to_mail,mbody)

			app_task(args=(msub,mbody,mfrom,mto))

			print("Account detail mailed")

			return True
		else:
			return False


	def add_app_approval_log(self,approval_level,action_by=None,mto=None,mail_status=True):
		app_approval_ins = AppApprovalLog()

		app_approval_ins.request_id = self.emp_ins.request_id
		app_approval_ins.app_id = self.app_ins

		if action_by:
			app_approval_ins.action_by = action_by

		if mto:
			app_approval_ins.mail_to = mto

		app_approval_ins.approval_level = approval_level
		app_approval_ins.mail_status = mail_status
		print("Saving ..............app approval log ......")
		app_approval_ins.save()

		return True

	def app_approval_status(self,level,status):
		

		app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = level,status=True).first()
		if app_appr_master:

			app_approval_ins = AppApprovalStatus.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins,approval_level=level).first()
			if not app_approval_ins:
				app_approval_ins=AppApprovalStatus()

				app_approval_ins.emp_id = self.emp_ins
				app_approval_ins.app_id = self.app_ins
				app_approval_ins.request_id = self.emp_ins.request_id
			app_approval_ins.approver = app_appr_master.approver_name
			app_approval_ins.approver_email=app_appr_master.approver_email
			app_approval_ins.approval_level = level
			app_approval_ins.approval_status = status
			app_approval_ins.mail_status = True
			app_approval_ins.save()

			return app_approval_ins
		else:
			return False

class AnthilApp:

	def __init__(self,emp_id,app_id):
		self.emp_id = emp_id
		self.app_id = app_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()
		self.app_ins=AppMaster.objects.filter(id=app_id).first()
		self.empapp_detail_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()

		# self.sn_mail = SYSMAIL

		# self.app_info_mail = SYSMAIL

	def approval_1(self):
		approval_level='1'

		
		sn = self.mail_to_sn(action=approval_level)
		if sn:
			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()
			print('EMP APP DEATIL ......ADMIN....INPROGRESS')


			return True
		else:
			return False
		
		
	def approval_2(self):
		approval_level='2'
		print("In create account.............")

		# self.add_app_approval_log(approval_level=APR_1_APD,action_by=SYSTEM,mto=None,mail_status=True)

		sn = self.mail_to_sn(action=approval_level)
		if sn:
			
			print('EMP APP DEATIL ......GAMIL....INPROGRESS')

			# self.add_app_approval_log(approval_level=ACC_REQ_SEND,action_by=SYSTEM,mto=self.sn_mail,mail_status=True)

			return True
		else:
			return False


	def approval_3(self):
		approval_level='3'
		if self.empapp_detail_ins.emp_app_status == ACTIVE:

			# self.add_app_approval_log(ACC_CREATED,self.sn_mail,mto=None,mail_status=True)

			sn=self.mail_to_sn(approval_level)
			if sn:
				return True
			else :
				return False
	
			# self.add_app_approval_log(ACC_CREDENT_SEND,SYSTEM,mto=self.sn_mail,mail_status=True)
		else:
			return False
			

	def check_bm_approval(self):
		emp_app_detail = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
		print("Check bm approval.......................")
		if emp_app_detail:
			if emp_app_detail.emp_app_status in [ACKL,'Active']:
				return True
			return False
		else:
			return False

		
	def mail_to_sn(self,action=None):
		ip=HOST
		approval_level=action



		if approval_level=='1':

			
			app_id = self.app_ins
			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)
				url = "http://{}/admin_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=self.empapp_detail_ins.id)

				msub="{0} app access rights for Employee code:{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)
				
				mbody="Please click on below link to Approve {0} application access rights for Employee http://{1}/app_info_holder/{2}/".format(self.app_ins.app_name,HOST,self.empapp_detail_ins.id)

				# mto = self.app_info_mail
				# mto = SYSMAIL
				mto = app_appr_master.approver_email
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				return False

		elif approval_level=='2':

			
			app_id = self.app_ins
			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()
			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)

				print("Sending mail to ..............sn anthil")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				url = "http://{}/emp_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee app detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,emp_app_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)

				

				# mto = SYSMAIL
				mto = app_appr_master.approver_email
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				return False


		elif approval_level == '3':

			#add_app_approval_log('APPROVAL_1_APPROVED',,mto=None,status=True)

			ip = HOST

			msub=""

			msub="{0} account created for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

			mbody="This is to inform you that  Account for Application :{0} has been Activated with User Name :{1} & Password : {2}".format(self.app_ins.app_name,self.empapp_detail_ins.app_login,self.empapp_detail_ins.app_pass)

			log_obj = AppLogCl(self.emp_ins.id)
			action="{} Account Created".format(self.app_ins.app_name)
			action_by ="Service Now"
			log_obj.create_log(action,action_by)

			# mto = SYSMAIL
			mto =self.emp_ins.reporting_authority_email   # mail goes to Reporting Authority
			# mto = SYSMAIL
			# mail_to_service_now(None,to_mail,mbody)
			mfrom=""

			app_task(args=(msub,mbody,mfrom,mto))

			return True
		else:
			return False


	def add_app_approval_log(self,approval_level,action_by=None,mto=None,mail_status=True):

		app_approval_ins = AppApprovalLog()
		app_approval_ins.request_id = self.emp_ins.request_id
		app_approval_ins.app_id = self.app_ins

		if action_by:
			app_approval_ins.action_by = action_by

		if mto:
			app_approval_ins.mail_to = mto

		app_approval_ins.approval_level = approval_level
		app_approval_ins.mail_status = mail_status
		print("Saving ..............app approval log ......")
		app_approval_ins.save()

		return True

	def app_approval_status(self,level,status):
		

		app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = level,status=True).first()
		if app_appr_master:

			app_approval_ins = AppApprovalStatus.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins,approval_level=level).first()
			if not app_approval_ins:
				app_approval_ins=AppApprovalStatus()

				app_approval_ins.emp_id = self.emp_ins
				app_approval_ins.app_id = self.app_ins
				app_approval_ins.request_id = self.emp_ins.request_id
			app_approval_ins.approver = app_appr_master.approver_name
			app_approval_ins.approver_email=app_appr_master.approver_email
			app_approval_ins.approval_level = level
			app_approval_ins.approval_status = status
			app_approval_ins.mail_status = True
			app_approval_ins.save()

			return app_approval_ins
		else:
			return False

class ErpApp:

	def __init__(self,emp_id,app_id):

		self.emp_id = emp_id
		self.app_id = app_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()
		self.app_ins=AppMaster.objects.filter(id=app_id).first()
		self.empapp_detail_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()

		self.sn_mail = SYSMAIL
		self.app_info_mail = SYSMAIL




	def approval_1(self):
		approval_level='1'

		
		sn = self.mail_to_sn(action=approval_level)
		if sn:
			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()
			print('EMP APP DEATIL ......ADMIN....INPROGRESS')

			# self.add_app_approval_log(approval_level=APR_1_SN,action_by=SYSTEM,mto=self.sn_mail,mail_status=True)

			return True
		else:
			return False
		


	def approval_2(self):
		approval_level='2'
		print("In create account.............")

		# self.add_app_approval_log(approval_level=APR_1_APD,action_by=SYSTEM,mto=None,mail_status=True)


		sn = self.mail_to_sn(action=approval_level)
		if sn:
			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()
			# print('EMP APP DEATIL ......ERP....INPROGRESS')

			# self.add_app_approval_log(approval_level=ACC_REQ_SEND,action_by=SYSTEM,mto=self.sn_mail,mail_status=True)

			return True
		else:
			return False


	def approval_3(self):
		approval_level='3'
		if self.empapp_detail_ins.emp_app_status == ACTIVE:

			# self.add_app_approval_log(ACC_CREATED,self.sn_mail,mto=None,mail_status=True)

			sn=self.mail_to_sn(approval_level)
			if sn:
				return True
			else:
				return False
		else:
			return False
	
			# self.add_app_approval_log(ACC_CREDENT_SEND,SYSTEM,mto=self.sn_mail,mail_status=True)

	def check_bm_approval(self):
		emp_app_detail = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
		print("Check bm approval.......................")
		if emp_app_detail:
			if emp_app_detail.emp_app_status in [ACKL,'Active']:
				return True
			return False
		else:
			return False

		
	def mail_to_sn(self,action=None):


		ip=HOST
		approval_level=action

		if approval_level=='1':
			
			app_id = self.app_ins
			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)
			
				url = "http://{}/admin_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=self.empapp_detail_ins.id)

				msub="{0} app access rights for Employee code:{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)
				
				mbody="Please click on below link to Approve {0} application access rights for Employee http://{1}/app_info_holder/{2}/".format(self.app_ins.app_name,HOST,self.empapp_detail_ins.id)

				# mto = self.app_info_mail
				mto = app_appr_master.approver_email
				# mto = SYSMAIL
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				return False

		elif approval_level=='2':
			
			app_id = self.app_ins

			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)
				print("Sending mail to ..............sn")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				url = "http://{}/emp_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee app detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,emp_app_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)

				mto = app_appr_master.approver_email
				# mto = SYSMAIL
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				return False


		elif approval_level=='3':



			#add_app_approval_log('APPROVAL_1_APPROVED',,mto=None,mail_status=True)

			ip = HOST

			msub=""

			msub="{0} account created for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

			mbody="This is to inform you that  Account for Application :{0} has been Activated with User Name :{1} & Password : {2}".format(self.app_ins.app_name,self.empapp_detail_ins.app_login,self.empapp_detail_ins.app_pass)

			log_obj = AppLogCl(self.emp_ins.id)
			action="{} Account Created".format(self.app_ins.app_name)
			action_by ="Service Now"
			log_obj.create_log(action,action_by)

			# mto = SYSMAIL
			mto =self.emp_ins.reporting_authority_email   # mail goes to Reporting Authority
			# mto = SYSMAIL
			# mail_to_service_now(None,to_mail,mbody)

			mfrom = ""

			app_task(args=(msub,mbody,mfrom,mto))

			return True
		else:
			return False


	def add_app_approval_log(self,approval_level,action_by=None,mto=None,mail_status=True):
		app_approval_ins = AppApprovalLog()

		app_approval_ins.request_id = self.emp_ins.request_id
		app_approval_ins.app_id = self.app_ins

		if action_by:
			app_approval_ins.action_by = action_by

		if mto:
			app_approval_ins.mail_to = mto

		app_approval_ins.approval_level = approval_level
		app_approval_ins.mail_status = mail_status
		print("Saving ..............app approval log ......")
		app_approval_ins.save()

		return True 

	def app_approval_status(self,level,status):
		

		app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = level,status=True).first()
		if app_appr_master:

			app_approval_ins = AppApprovalStatus.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins,approval_level=level).first()
			if not app_approval_ins:
				app_approval_ins=AppApprovalStatus()

				app_approval_ins.emp_id = self.emp_ins
				app_approval_ins.app_id = self.app_ins
				app_approval_ins.request_id = self.emp_ins.request_id
			app_approval_ins.approver = app_appr_master.approver_name
			app_approval_ins.approver_email=app_appr_master.approver_email
			app_approval_ins.approval_level = level
			app_approval_ins.approval_status = status
			app_approval_ins.mail_status = True
			app_approval_ins.save()

			return app_approval_ins
		else:
			return False

class DspApp:

	def __init__(self,emp_id,app_id):
		self.emp_id = emp_id
		self.app_id = app_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()
		self.app_ins=AppMaster.objects.filter(id=app_id).first()
		self.empapp_detail_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()

		self.sn_mail = SYSMAIL

		self.hr_mail = SYSMAIL

	# mail to hr for approval...........
	def approval_1(self):
		approval_level='1'
		print("In create account.............")

		# app_approval_log = AppApprovalLog.objects.filter(app_id=self.app_ins,request_id=self.emp_ins.request_id,approval_level = APR_1_SN,mail_status = True).first()
		
		sn = self.mail_to_sn(action=approval_level)
		self.app_approval_status(level=1,status='PENDING')
		
		if sn:


			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()
			self.app_approval_status(level=1,status='APPROVED')


			self.approval_2()
			
				

			print('EMP APP DEATIL ......DSP....INPROGRESS')

			# self.add_app_approval_log(approval_level=APR_1_SN,action_by=SYSTEM,mto=self.hr_mail,mail_status=True)

			return True
		else:
			self.app_approval_status(level=1,status='FAILED')
			return False

	def approval_2(self):
		approval_level='2'
		print("In create account.............")

		# app_approval_log = AppApprovalLog.objects.filter(app_id=self.app_ins,request_id=self.emp_ins.request_id,approval_level = APR_1_SN,mail_status = True).first()		

		sn = self.mail_to_sn(action=approval_level)
		
		if sn:
			
			self.app_approval_status(level=2,status='PENDING')
			print('EMP APP DEATIL ......DSP....INPROGRESS')

			# self.add_app_approval_log(approval_level=APR_1_SN,action_by=SYSTEM,mto=self.hr_mail,mail_status=True)

			return True
		else:
			self.app_approval_status(level=2,status='FAILED')
			return False

	# def acc_creation(self):

	# 	if self.check_bm_approval():

	# 		app_approval_log = AppApprovalLog.objects.filter(app_id=self.app_ins,request_id=self.emp_ins.request_id,approval_level = APR_1_RJD,mail_status = True).first()

	# 		if not app_approval_log:

	# 			sn = self.mail_to_sn(action='NEWACCOUNT')
	# 			if sn:
					
	# 				print('EMP APP  ......ICAB ....INPROGRESS')

	# 				self.add_app_approval_log(approval_level=ACC_REQ_SEND,action_by=SYSTEM,mto=self.sn_mail,mail_status=True)

	# 				return True
	# 		else:
	# 			return False



	def approval_3(self):
		approval_level = '3'


		if self.empapp_detail_ins.emp_app_status == ACTIVE:

			# self.add_app_approval_log(ACC_CREATED,self.sn_mail,mto=None,mail_status=True)

			self.mail_to_sn(approval_level)
	
			# self.add_app_approval_log(ACC_CREDENT_SEND,SYSTEM,mto=self.sn_mail,mail_status=True)
			return True
		else:
			return False


	def check_bm_approval(self):
		emp_app_detail = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
		print("Check bm approval.......................")
		if emp_app_detail:
			if emp_app_detail.emp_app_status in [ACKL,'Active']:
				return True
			return False
		else:
			return False

		
	def mail_to_sn(self,action=None):

		ip= HOST

		approval_level=action


		if approval_level=='1':
			approver_level = '1'
			app_id = self.app_ins
			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)
				print("Sending mail to ..............DSP")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				ip = HOST
				msub=""
				msub="{0} account for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)
				mbody="This is to inform you that  Reporting authority requested  {0} account creation for employee code {1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

				# mto = SYSMAIL
				mto = app_appr_master.approver_email
				# mto = SYSMAIL
				# mail_to_service_now(None,to_mail,mbody)

				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))

				return True
			else:
				return False
		

		elif approval_level=='2':
			approval_level = '2'
			app_id = self.app_ins

			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)
				print("Sending mail to ..............dsp")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				url = "http://{}/dsp_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee app detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,emp_app_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)

				mto = app_appr_master.approver_email
				# mto = SYSMAIL
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				pass


		elif approval_level=='3':



			#add_app_approval_log('APPROVAL_1_APPROVED',,mto=None,mail_status=True)

			ip = HOST

			msub=""

			msub="{0} account created for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

			mbody="This is to inform you that  Account for Application :{0} has been Activated with User Name <Rentokil-pci email id>  & Password <employee code>".format(self.app_ins.app_name)

			log_obj = AppLogCl(self.emp_ins.id)
			action="{} Account Created".format(self.app_ins.app_name)
			action_by ="Service Now"
			log_obj.create_log(action,action_by)

			# mto = SYSMAIL
			mto =self.emp_ins.reporting_authority_email   # mail goes to Reporting Authority
			# mto = SYSMAIL
			# mail_to_service_now(None,to_mail,mbody)

			mfrom = ""

			app_task(args=(msub,mbody,mfrom,mto))
			return True

		else:
			return False


	def add_app_approval_log(self,approval_level,action_by=None,mto=None,mail_status=True):
		app_approval_ins = AppApprovalLog()

		app_approval_ins.request_id = self.emp_ins.request_id
		app_approval_ins.app_id = self.app_ins

		if action_by:
			app_approval_ins.action_by = action_by

		if mto:
			app_approval_ins.mail_to = mto

		app_approval_ins.approval_level = approval_level
		app_approval_ins.mail_status = mail_status
		print("Saving ..............app approval log ......")
		app_approval_ins.save()

		return True 

	def app_approval_status(self,level,status):
		

		app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = level,status=True).first()
		if app_appr_master:

			app_approval_ins = AppApprovalStatus.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins,approval_level=level).first()
			if not app_approval_ins:
				app_approval_ins=AppApprovalStatus()

				app_approval_ins.emp_id = self.emp_ins
				app_approval_ins.app_id = self.app_ins
				app_approval_ins.request_id = self.emp_ins.request_id
			app_approval_ins.approver = app_appr_master.approver_name
			app_approval_ins.approver_email=app_appr_master.approver_email
			app_approval_ins.approval_level = level
			app_approval_ins.approval_status = status
			app_approval_ins.mail_status = True
			app_approval_ins.save()

			return app_approval_ins
		else:
			return False

class ICabsApp:

	def __init__(self,emp_id,app_id):
		self.emp_id = emp_id
		self.app_id = app_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()
		self.app_ins=AppMaster.objects.filter(id=app_id).first()
		self.empapp_detail_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()

		self.sn_mail = SYSMAIL

		self.hr_mail = SYSMAIL
		self.app_info_mail = SYSMAIL


	def approval_1(self):
		approval_level='1'

		sn = self.mail_to_sn(action=approval_level)
		if sn:
			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()
			print('EMP APP DEATIL ......ADMIN....INPROGRESS')

			# self.add_app_approval_log(approval_level=APR_1_SN,action_by=SYSTEM,mto=self.sn_mail,mail_status=True)

			return True
		else:
			return False
		

	# mail to hr for approval...........
	def approval_2(self):
		approval_level = '2'
		print("In create account.............")

		
		# self.add_app_approval_log(approval_level=APR_1_APD,action_by=SYSTEM,mto=None,mail_status=True)
	
		
		sn = self.mail_to_sn(action=approval_level)
		if sn:

			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()

			print('EMP APP DEATIL ......ICAB....INPROGRESS')

			# self.add_app_approval_log(approval_level=ACC_REQ_SEND,action_by=SYSTEM,mto=self.hr_mail,mail_status=True)

			return True
		else:
			return False


	# def acc_creation(self):

	# 	if self.check_bm_approval():

	# 		app_approval_log = AppApprovalLog.objects.filter(app_id=self.app_ins,request_id=self.emp_ins.request_id,approval_level = APR_1_RJD,mail_status = True).first()

	# 		if not app_approval_log:

	# 			sn = self.mail_to_sn(action='NEWACCOUNT')
	# 			if sn:
					
	# 				print('EMP APP  ......ICAB ....INPROGRESS')

	# 				self.add_app_approval_log(approval_level=ACC_REQ_SEND,action_by=SYSTEM,mto=self.sn_mail,mail_status=True)

	# 				return True
	# 		else:
	# 			return False



	def approval_3(self):
		approval_level='3'

		if self.empapp_detail_ins.emp_app_status == ACTIVE:

			# self.add_app_approval_log(ACC_CREATED,self.sn_mail,mto=None,mail_status=True)

			self.mail_to_sn(approval_level)
	
			# self.add_app_approval_log(ACC_CREDENT_SEND,SYSTEM,mto=self.sn_mail,mail_status=True)
			return True
		else:
			return False

	def check_bm_approval(self):
		emp_app_detail = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
		print("Check bm approval.......................")
		if emp_app_detail:
			if emp_app_detail.emp_app_status in [ACKL,'Active']:
				return True
			return False
		else:
			return False

		
	def mail_to_sn(self,action=None):

		ip=HOST

		approval_level = action

		if approval_level=='1':
			approver_level = '1'
			app_id = self.app_ins

			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)

				url = "http://{}/admin_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=self.empapp_detail_ins.id)

				msub="{0} app access rights for Employee code:{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)
				
			


				mbody="Please click on below link to Approve {0} application access rights for Employee http://{1}/app_info_holder/{2}/".format(self.app_ins.app_name,HOST,self.empapp_detail_ins.id)


				# mto = self.app_info_mail
				mto = app_appr_master.approver_email
				# mto = SYSMAIL
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				# return True
			
	
				#......Mail  to inform HR................... 
			
				print("Sending mail to ..............ICAB")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				ip = HOST
				msub=""
				msub="{0} account for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)
				mbody="This is to inform you that  Reporting authority requested  {0} account creation for employee code {1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

				mto = app_appr_master.approver_email
				# mto = SYSMAIL
				# mail_to_service_now(None,to_mail,mbody)

				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))

				return True
			else:
				return False
		

		elif approval_level=='2':
			approver_level = '2'
			app_id = self.app_ins

			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)
				print("Sending mail to ..............sn")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				url = "http://{}/emp_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee app detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,emp_app_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)

				mto = SYSMAIL
				# mto = SYSMAIL
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				return False


		elif approval_level=='3':

			#add_app_approval_log('APPROVAL_1_APPROVED',,mto=None,mail_status=True)

			ip = HOST

			msub=""

			msub="{0} account created for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

			mbody="This is to inform you that  Account for Application :{0} has been Activated with User Name :{1} & Password : {2}".format(self.app_ins.app_name,self.empapp_detail_ins.app_login,self.empapp_detail_ins.app_pass)

			log_obj = AppLogCl(self.emp_ins.id)
			action="{} Account Created".format(self.app_ins.app_name)
			action_by ="Service Now"
			log_obj.create_log(action,action_by)

			mto =self.emp_ins.reporting_authority_email   # mail goes to Reporting Authority
			# mto = SYSMAIL
			# mail_to_service_now(None,to_mail,mbody)

			mfrom = ""

			app_task(args=(msub,mbody,mfrom,mto))

			return True


		else:
			return False


	def add_app_approval_log(self,approval_level,action_by=None,mto=None,mail_status=True):
		app_approval_ins = AppApprovalLog()

		app_approval_ins.request_id = self.emp_ins.request_id
		app_approval_ins.app_id = self.app_ins

		if action_by:
			app_approval_ins.action_by = action_by

		if mto:
			app_approval_ins.mail_to = mto

		app_approval_ins.approval_level = approval_level
		app_approval_ins.mail_status = mail_status
		print("Saving ..............app approval log ......")
		app_approval_ins.save()

		return True 


	def app_approval_status(self,level,status):
		
		app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = level,status=True).first()
		if app_appr_master:

			app_approval_ins = AppApprovalStatus.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins,approval_level=level).first()
			if not app_approval_ins:
				app_approval_ins=AppApprovalStatus()

				app_approval_ins.emp_id = self.emp_ins
				app_approval_ins.app_id = self.app_ins
				app_approval_ins.request_id = self.emp_ins.request_id
			app_approval_ins.approver = app_appr_master.approver_name
			app_approval_ins.approver_email=app_appr_master.approver_email
			app_approval_ins.approval_level = level
			app_approval_ins.approval_status = status
			app_approval_ins.mail_status = True
			app_approval_ins.save()

			return app_approval_ins
		else:
			return False


class NavApp:

	def __init__(self,emp_id,app_id):
		self.emp_id = emp_id
		self.app_id = app_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()
		self.app_ins=AppMaster.objects.filter(id=app_id).first()
		self.empapp_detail_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()

		self.sn_mail = SYSMAIL
		self.hod_mail = SYSMAIL

   # first approval
	def approval_1(self):
		approval_level='1'
		print("In create account.............")

		# if self.check_bm_approval():

		# 	app_approval_log = AppApprovalLog.objects.filter(app_id=self.app_ins,request_id=self.emp_ins.request_id,approval_level = APR_1_SN,mail_status = True).first()

		# 	if not app_approval_log:

		nav = self.nav_app_approval(action=approval_level)
		
		if nav:
			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()
			
			# self.add_app_approval_log(approval_level=APR_1_SN,action_by=SYSTEM,mto=self.hod_mail,mail_status=True)

			return True
		else:
			return False


	def approval_3(self): #account_created

		approval_level = '3'
		if self.empapp_detail_ins.emp_app_status ==ACTIVE:
			# self.add_app_approval_log(approval_level=APR_1_APD,action_by=SYSTEM,mto=self.hod_mail,mail_status=True)

			# self.add_app_approval_log(ACC_CREATED,self.sn_mail,mto=None,mail_status=True)

			sn=self.mail_to_sn(approval_level)
			if sn:
				return True
			else:
				return False
	
			# self.add_app_approval_log('ACC_CREDENT_SEND','SYSTEM',mto=self.sn_mail,mail_status=True)
		else:
			return False

			

	def check_bm_approval(self):
		emp_app_detail = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
		print("Check bm approval.......................")
		if emp_app_detail:
			if emp_app_detail.emp_app_status in [ACKL]:
				return True
			return False
		else:
			return False

	
	def nav_app_approval(self,action=None):
		approval_level=action

		if approval_level == '1':
			print("Sending mail to ..............HOD")

			if self.empapp_detail_ins:

				app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

				if app_appr_master:

					access_type = self.empapp_detail_ins.app_access_types

					ip = HOST

					
					msub="Navision app access rights for Employee code:{}".format(self.emp_ins.emp_code)
					mbody="Please click on below link to Approve Navision app access rights for Employee http://{0}/nav_access_approval/{1}/{2}/".format(HOST,self.emp_ins.emp_code,self.app_ins.id)

					mto = app_appr_master.approver_email
					mfrom = ""

					app_task(args=(msub,mbody,mfrom,mto))
				else:
					return False

				
			else:
				return False
		else:
			return False

	def mail_to_sn(self,action=None):

		ip=HOST

		approval_level=action

		if approval_level=='2':

			approval_level='2'

			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			# self.add_app_approval_log(approval_level=APR_1_APD,action_by=self.hod_mail,mto=None,mail_status=True)

			if app_appr_master:

				log_obj = AppLogCl(self.emp_ins.id)
				action="HOD approved for {} app".format(self.app_ins.app_name)
				action_by =self.hod_mail
				log_obj.create_log(action,action_by)

				print("Sending mail to ..............sn")
				
				url = "http://{}/nav_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=self.empapp_detail_ins.id)

				msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee app detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,self.empapp_detail_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)

				mto = app_appr_master.approver_email
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				
				# self.add_app_approval_log(approval_level=ACC_REQ_SEND,action_by=SYSTEM,mto=self.sn_mail,mail_status=True)
				return True
			else:
				return False


		elif approval_level=='3':
			# self.add_app_approval_log(approval_level=ACC_CREATED,action_by=self.sn_mail,mto=None,mail_status=True)

			#add_app_approval_log('APPROVAL_1_APPROVED',,mto=None,mail_status=True)


			ip = HOST

			msub=""

			msub="{0} account created for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

			mbody="This is to inform you that  Account for Application :{0} has been Activated with User Name :{1} & Password : {2}".format(self.app_ins.app_name,self.empapp_detail_ins.app_login,self.empapp_detail_ins.app_pass)


			log_obj = AppLogCl(self.emp_ins.id)
			action="{} Account Created".format(self.app_ins.app_name)
			action_by ="Service Now"
			log_obj.create_log(action,action_by)

			mto = self.emp_ins.reporting_authority_email

			mfrom = ""

			app_task(args=(msub,mbody,mfrom,mto))

			# self.add_app_approval_log(approval_level=ACC_CREDENT_SEND,action_by=SYSTEM,mto=self.sn_mail,mail_status=True)

			return True
		else:
			return False


	def add_app_approval_log(self,approval_level,action_by=None,mto=None,mail_status=True):
		app_approval_ins = AppApprovalLog()

		app_approval_ins.request_id = self.emp_ins.request_id
		app_approval_ins.app_id = self.app_ins

		if action_by:
			app_approval_ins.action_by = action_by

		if mto:
			app_approval_ins.mail_to = mto

		app_approval_ins.approval_level = approval_level
		app_approval_ins.mail_status = mail_status
		print("Saving ..............app approval log ......")
		app_approval_ins.save()

		return True		

	def app_approval_status(self,level,status):
		
		app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = level,status=True).first()
		if app_appr_master:

			app_approval_ins = AppApprovalStatus.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins,approval_level=level).first()
			if not app_approval_ins:
				app_approval_ins=AppApprovalStatus()

				app_approval_ins.emp_id = self.emp_ins
				app_approval_ins.app_id = self.app_ins
				app_approval_ins.request_id = self.emp_ins.request_id
			app_approval_ins.approver = app_appr_master.approver_name
			app_approval_ins.approver_email=app_appr_master.approver_email
			app_approval_ins.approval_level = level
			app_approval_ins.approval_status = status
			app_approval_ins.mail_status = True
			app_approval_ins.save()

			return app_approval_ins
		else:
			return False


class STPApp:

	def __init__(self,emp_id,app_id):

		self.emp_id = emp_id
		self.app_id = app_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()
		self.app_ins=AppMaster.objects.filter(id=app_id).first()
		self.empapp_detail_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()

		self.sn_mail = SYSMAIL
		self.APR_1_MAIL = SYSMAIL
		self.APR_2_MAIL = SYSMAIL



	def approval_1(self):

		print("In create account........STP...approval_1..")
		approval_level = '1'
		
		sn = self.mail_to_sn(action=approval_level)
		if sn:
			# self.add_app_approval_log(approval_level=APR_1_SN,action_by='SYSTEM',mto=self.APR_1_MAIL,status=True)
			self.empapp_detail_ins.emp_app_status = INPROGRESS
			self.empapp_detail_ins.save()

			return True
		else:
			return False


	def approval_2(self):

		approval_level = '2'

		print("In create account..........2 st...")

		# self.add_app_approval_log(approval_level=APR_1_APD,action_by='SYSTEM',mto='',status=True)

		# app_approval_log = AppApprovalLog.objects.filter(app_id=self.app_ins,request_id=self.emp_ins.request_id,approval_level = APR_2_SN,mail_status = True).first()

		print("In second approval")

		sn = self.mail_to_sn(action=approval_level)

		if sn:
			# self.add_app_approval_log(approval_level=APR_2_SN,action_by='SYSTEM',mto=self.APR_1_MAIL,status=True)
			self.empapp_detail_ins.emp_app_status = INPROGRESS
			self.empapp_detail_ins.save()

			return True
		else:
			return False
			

	def acc_created(self):

		approval_level='3'
		if self.empapp_detail_ins.emp_app_status ==ACTIVE:

			# self.add_app_approval_log('ACC_CREATED',self.sn_mail,mto=None,status=True)

			sn=self.mail_to_sn(approval_level)

			if sn:
				return True
			else:
				return False
	
			# self.add_app_approval_log('ACC_CREDENT_SEND','SYSTEM',mto=self.sn_mail,status=True)

		else:
			return False

	def check_bm_approval(self):

		emp_app_detail = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
		print("Check bm approval.......................")
		
		if emp_app_detail:
			if emp_app_detail.emp_app_status in ['Acknowledged']:
				return True
			return False
		else:
			return False


	def mail_to_opex(self,action=None):

		if action=='NEWACCOUNT':
			print("Sending mail to ..............stp")

			emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
			
			url = "http://{}/emp_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

			msub="Request for STP app access"

			# msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

			mbody="Request ID:{} ,STP app access request for employee code :{}.".format(self.emp_ins.request_id.id,self.emp_ins.emp_code)

			mto = SYSMAIL
			mto = self.sn_mail
			mfrom = ""

			app_task(args=(msub,mbody,mfrom,mto))
			return True


		
	def mail_to_sn(self,action=None):

		approval_level = action

		if approval_level=='1':
			print("Sending mail to ..............stp")

			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				url = "http://{}/stp_app_from/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				msub="Request for STP app access"

				# msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				mbody="Request ID:{} ,STP app access request for employee code :{}.".format(self.emp_ins.request_id.id,self.emp_ins.emp_code)

				
				mto =app_appr_master.approver_email
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				return False

		elif approval_level=='2':

			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:

				print("Sending mail to .........st.....sn")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				url = "http://{}/app_stp_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				msub="STP app installation for Employee code {} ".format(self.emp_ins.emp_code)

				mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,emp_app_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)
				
				mto = app_appr_master.approver_email
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				return False


		elif approval_level=='3': # ACC_CREATED



			#add_app_approval_log('APPROVAL_1_APPROVED',,mto=None,status=True)

			ip = HOST

			msub=""

			msub="{0} account created for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

			mbody="This is to inform you that  Account for Application :{0} has been Activated with User Name :{1} & Password : {2}".format(self.app_ins.app_name,self.empapp_detail_ins.app_login,self.empapp_detail_ins.app_pass)

			
			# mail_to_service_now(None,to_mail,mbody)
			mto = self.emp_ins.reporting_authority_email
			app_task(args=(msub,mbody,mfrom,mto))

			return True

		else:
			return False



	def add_app_approval_log(self,approval_level,action_by=None,mto=None,status=True):
		app_approval_ins = AppApprovalLog()

		app_approval_ins.request_id = self.emp_ins.request_id
		app_approval_ins.app_id = self.app_ins

		if action_by:
			app_approval_ins.action_by = action_by

		if mto:
			app_approval_ins.mail_to = mto

		app_approval_ins.approval_level = approval_level
		app_approval_ins.mail_status = status
		print("Saving ..............app approval log ......")
		app_approval_ins.save()

		return True

	def app_approval_status(self,level,status):
		

		app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = level,status=True).first()
		if app_appr_master:

			app_approval_ins = AppApprovalStatus.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins,approval_level=level).first()
			if not app_approval_ins:
				app_approval_ins=AppApprovalStatus()

				app_approval_ins.emp_id = self.emp_ins
				app_approval_ins.app_id = self.app_ins
				app_approval_ins.request_id = self.emp_ins.request_id
			app_approval_ins.approver = app_appr_master.approver_name
			app_approval_ins.approver_email=app_appr_master.approver_email
			app_approval_ins.approval_level = level
			app_approval_ins.approval_status = status
			app_approval_ins.mail_status = True
			app_approval_ins.save()

			return app_approval_ins
		else:
			return False


class iAuditorApp:

	def __init__(self,emp_id,app_id):
		self.emp_id = emp_id
		self.app_id = app_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()
		self.app_ins=AppMaster.objects.filter(id=app_id).first()
		self.empapp_detail_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()

		# self.sn_mail = SYSMAIL

		# self.app_info_mail = SYSMAIL


	def approval_1(self):
		approval_level='1'


		print('EMP...iAuditorApp...ADMIN....INPROGRESS')


		sn = self.mail_to_sn(action=approval_level)
		if sn:
			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()

			print('EMP APP DEATIL ...iAuditorApp...ADMIN....INPROGRESS')

			return True
		else:
			return False
		


	def approval_2(self):

		approval_level='2'
		print("In create account.............")
		sn = self.mail_to_sn(action=approval_level)

		if sn:
			print('EMP APP DEATIL ......GAMIL....INPROGRESS')
			return True
		else:
			return False
	

	def approval_3(self):

		approval_level='3'

		if self.empapp_detail_ins.emp_app_status == ACTIVE:

			# self.add_app_approval_log(ACC_CREATED,self.sn_mail,mto=None,mail_status=True)
			sn=self.mail_to_sn(approval_level)

			if sn:
				return True
			else :
				return False

			# self.add_app_approval_log(ACC_CREDENT_SEND,SYSTEM,mto=self.sn_mail,mail_status=True)
		
		else:
			return False

	def check_bm_approval(self):
		emp_app_detail = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
		print("Check bm approval.......................")
		if emp_app_detail:
			if emp_app_detail.emp_app_status in [ACKL]:
				return True
			return False
		else:
			return False

		
	def mail_to_sn(self,action=None):

		ip=HOST
		approval_level=action

		

		if approval_level=='1':

			print("In approval .....iAuditorApp")
 
			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()
			print("In approval .....iAuditorApp {}".format(app_appr_master))
			if app_appr_master:
				print("Sending mail to ..............sn")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				# url = "http://{}/emp_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				# msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				# mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee app detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,emp_app_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)

				
				url = "http://{}/emp_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee app detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,emp_app_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)


				mto = app_appr_master.approver_email    # mail goes to Service Now
				# mto = SYSMAIL
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				return False


		elif approval_level=='2':

			#add_app_approval_log('APPROVAL_1_APPROVED',,mto=None,mail_status=True)

			ip = HOST

			msub="{0} account created for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

			mbody="This is to inform you that  Account for Application :{0} has been Activated with User Name :{1} & Password : {2}".format(self.app_ins.app_name,self.empapp_detail_ins.app_login,self.empapp_detail_ins.app_pass)

			log_obj = AppLogCl(self.emp_ins.id)
			action="{} Account Created".format(self.app_ins.app_name)
			action_by ="Service Now"
			log_obj.create_log(action,action_by)

			# mto =self.sn_mail
			mto =self.emp_ins.reporting_authority_email   # mail goes to Reporting Authority
			mfrom = ''
			# to_mail = SYSMAIL
			# mail_to_service_now(None,to_mail,mbody)

			app_task(args=(msub,mbody,mfrom,mto))

			print("Account detail mailed")

			return True
		else:
			return False


	def add_app_approval_log(self,approval_level,action_by=None,mto=None,mail_status=True):
		app_approval_ins = AppApprovalLog()

		app_approval_ins.request_id = self.emp_ins.request_id
		app_approval_ins.app_id = self.app_ins

		if action_by:
			app_approval_ins.action_by = action_by

		if mto:
			app_approval_ins.mail_to = mto

		app_approval_ins.approval_level = approval_level
		app_approval_ins.mail_status = mail_status
		print("Saving ..............app approval log ......")
		app_approval_ins.save()

		return True

	def app_approval_status(self,level,status):

		approver_name = None
		approver_email = None

		

		app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = level,status=True).first()
		
		if app_appr_master:
			approver_name = app_appr_master.approver_name or None
			approver_email = app_appr_master.approver_email or  None

		app_approval_ins = AppApprovalStatus.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins,approval_level=level).first()

		if not app_approval_ins:
			app_approval_ins=AppApprovalStatus()

		app_approval_ins.emp_id = self.emp_ins
		app_approval_ins.app_id = self.app_ins
		app_approval_ins.request_id = self.emp_ins.request_id

		app_approval_ins.approver = approver_name or None
		app_approval_ins.approver_email= approver_email or None
		app_approval_ins.approval_level = level
		app_approval_ins.approval_status = status
		app_approval_ins.mail_status = True
		app_approval_ins.save()

		return app_approval_ins



class SPAApp:

	def __init__(self,emp_id,app_id):
		self.emp_id = emp_id
		self.app_id = app_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()
		self.app_ins=AppMaster.objects.filter(id=app_id).first()
		self.empapp_detail_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()

		self.sn_mail = SYSMAIL

		self.hr_mail = SYSMAIL

	# mail to hr for approval...........
	def approval_1(self):
		approval_level='1'
		print("In create account.............")

		# app_approval_log = AppApprovalLog.objects.filter(app_id=self.app_ins,request_id=self.emp_ins.request_id,approval_level = APR_1_SN,mail_status = True).first()
		
		sn = self.mail_to_sn(action=approval_level)
		self.app_approval_status(level=1,status='PENDING')
		
		if sn:


			self.empapp_detail_ins.emp_app_status=INPROGRESS
			self.empapp_detail_ins.save()
			self.app_approval_status(level=1,status='APPROVED')


			self.approval_2()
			
				

			print('EMP APP DEATIL ......SPA....INPROGRESS')

			# self.add_app_approval_log(approval_level=APR_1_SN,action_by=SYSTEM,mto=self.hr_mail,mail_status=True)

			return True
		else:
			self.app_approval_status(level=1,status='FAILED')
			return False

	def approval_2(self):
		approval_level='2'
		print("In create account.............")

		# app_approval_log = AppApprovalLog.objects.filter(app_id=self.app_ins,request_id=self.emp_ins.request_id,approval_level = APR_1_SN,mail_status = True).first()		

		sn = self.mail_to_sn(action=approval_level)
		
		if sn:
			
			self.app_approval_status(level=2,status='PENDING')
			print('EMP APP DEATIL ......SPA....INPROGRESS')

			# self.add_app_approval_log(approval_level=APR_1_SN,action_by=SYSTEM,mto=self.hr_mail,mail_status=True)

			return True
		else:
			self.app_approval_status(level=2,status='FAILED')
			return False

	# def acc_creation(self):

	# 	if self.check_bm_approval():

	# 		app_approval_log = AppApprovalLog.objects.filter(app_id=self.app_ins,request_id=self.emp_ins.request_id,approval_level = APR_1_RJD,mail_status = True).first()

	# 		if not app_approval_log:

	# 			sn = self.mail_to_sn(action='NEWACCOUNT')
	# 			if sn:
					
	# 				print('EMP APP  ......ICAB ....INPROGRESS')

	# 				self.add_app_approval_log(approval_level=ACC_REQ_SEND,action_by=SYSTEM,mto=self.sn_mail,mail_status=True)

	# 				return True
	# 		else:
	# 			return False



	def approval_3(self):
		approval_level = '3'


		if self.empapp_detail_ins.emp_app_status == ACTIVE:

			# self.add_app_approval_log(ACC_CREATED,self.sn_mail,mto=None,mail_status=True)

			self.mail_to_sn(approval_level)
	
			# self.add_app_approval_log(ACC_CREDENT_SEND,SYSTEM,mto=self.sn_mail,mail_status=True)
			return True
		else:
			return False


	def check_bm_approval(self):
		emp_app_detail = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
		print("Check bm approval.......................")
		if emp_app_detail:
			if emp_app_detail.emp_app_status in [ACKL,'Active']:
				return True
			return False
		else:
			return False

		
	def mail_to_sn(self,action=None):

		ip= HOST

		approval_level=action


		if approval_level=='1':
			approver_level = '1'
			app_id = self.app_ins
			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)
				print("Sending mail to ..............SPA")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				ip = HOST
				msub=""
				msub="{0} account for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)
				mbody="This is to inform you that  Reporting authority requested  {0} account creation for employee code {1}".format(self.app_ins.app_name,self.emp_ins.emp_code)

				# mto = SYSMAIL
				mto = app_appr_master.approver_email
				# mto = SYSMAIL
				# mail_to_service_now(None,to_mail,mbody)

				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))

				return True
			else:
				return False
		

		elif approval_level=='2':
			approval_level = '2'
			app_id = self.app_ins

			app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = approval_level,status=True).first()

			if app_appr_master:
				print('--app_appr_master----',app_appr_master.approver_email)
				print("Sending mail to ..............spa")

				emp_app_ins = EmpAppDetail.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins).first()
				
				url = "http://{}/spa_app_detail/{emp_app_detail}/".format(HOST,emp_app_detail=emp_app_ins.id)

				msub="Employee {} {} got approved".format(self.emp_ins.emp_fname, self.emp_ins.emp_lname)

				mbody="Request ID: {}. Create {} account for following employee. Role: {}. Employee Details : {}, {}, {}, {}, {}  is approved. Please click on below link to see employee app detail {}".format(self.emp_ins.request_id.request_id,self.app_ins.app_name,emp_app_ins.app_access_types,self.emp_ins.emp_code,self.emp_ins.emp_fname,self.emp_ins.emp_lname,self.emp_ins.emp_mobile,self.emp_ins.emp_email,url)

				mto = app_appr_master.approver_email
				# mto = SYSMAIL
				mfrom = ""

				app_task(args=(msub,mbody,mfrom,mto))
				return True
			else:
				pass


		elif approval_level=='3':

			#add_app_approval_log('APPROVAL_1_APPROVED',,mto=None,mail_status=True)

			ip = HOST
			msub=""
			msub="{0} account created for employee code :{1}".format(self.app_ins.app_name,self.emp_ins.emp_code)
			mbody="This is to inform you that  Account for Application :{0} has been Activated with User Name : < Rentokil-pci email id >  & Password:< employee code >".format(self.app_ins.app_name)

			log_obj = AppLogCl(self.emp_ins.id)
			action="{} Account Created".format(self.app_ins.app_name)
			action_by ="Service Now"
			log_obj.create_log(action,action_by)

			# mto = SYSMAIL
			mto =self.emp_ins.reporting_authority_email   # mail goes to Reporting Authority
			# mto = SYSMAIL
			# mail_to_service_now(None,to_mail,mbody)

			mfrom = ""
			app_task(args=(msub,mbody,mfrom,mto))
			return True
		else:
			return False


	def add_app_approval_log(self,approval_level,action_by=None,mto=None,mail_status=True):
		app_approval_ins = AppApprovalLog()

		app_approval_ins.request_id = self.emp_ins.request_id
		app_approval_ins.app_id = self.app_ins

		if action_by:
			app_approval_ins.action_by = action_by

		if mto:
			app_approval_ins.mail_to = mto

		app_approval_ins.approval_level = approval_level
		app_approval_ins.mail_status = mail_status
		print("Saving ..............app approval log ......")
		app_approval_ins.save()

		return True 

	def app_approval_status(self,level,status):
		

		app_appr_master = AppApproverMaster.objects.filter(app_id=self.app_ins,approver_level = level,status=True).first()
		if app_appr_master:

			app_approval_ins = AppApprovalStatus.objects.filter(emp_id=self.emp_ins,app_id=self.app_ins,approval_level=level).first()
			if not app_approval_ins:
				app_approval_ins=AppApprovalStatus()

				app_approval_ins.emp_id = self.emp_ins
				app_approval_ins.app_id = self.app_ins
				app_approval_ins.request_id = self.emp_ins.request_id
			app_approval_ins.approver = app_appr_master.approver_name
			app_approval_ins.approver_email=app_appr_master.approver_email
			app_approval_ins.approval_level = level
			app_approval_ins.approval_status = status
			app_approval_ins.mail_status = True
			app_approval_ins.save()

			return app_approval_ins
		else:
			return False






class AppLogCl:

	def __init__(self,emp_id):

		self.emp_id = emp_id
		self.emp_ins=EmployeeMaster.objects.filter(id=emp_id).first()

	def create_log(self,action,action_by):
		app_log_ins = AppLog()

		app_log_ins.emp_id = self.emp_ins
		app_log_ins.request_id = self.emp_ins.request_id
		app_log_ins.action = action
		app_log_ins.action_by = action_by

		app_log_ins.save()

		print("Log creation ...{}".format(action))
		return True

class LeaveAttendanceLogCl:

	def __init__(self,lev_id):

		self.lev_id = lev_id
		self.lev_ins=LeaveMaster.objects.filter(id=lev_id).first()

	def create_log(self,action,action_by):
		app_log_ins = LeaveAttendanceLog()

		app_log_ins.lev_id = self.lev_ins
		app_log_ins.action = action
		app_log_ins.action_by = action_by

		app_log_ins.save()

		print("---------Log creation ...{}".format(action))
		return True

class LocationCl:
	def __init__(self,location_id,location_type):
		self.location_id = location_id
		self.location_type = location_type
		self.location_name = None


	def getLocation(self):

		if self.location_type =='VERTICAL':
			vertical_id = VerticalMaster.objects.filter(id=self.location_id ).first()
			self.location_name = vertical_id.vt_name

		if self.location_type=='REGION':
			region_id = RegionMaster.objects.filter(id=self.location_id ).first()
			vertical_id = region_id.vertical_id
			self.location_name = region_id.rg_name

		if self.location_type=='DIVISION':
			division_id = DesignationMaster.objects.filter(id=self.location_id ).first()
			region_id = division_id.region_id
			vertical_id = region_id.vertical_id

			self.location_name = division_id.div_name


		if self.location_type=='BRANCH':
			branch_id = BranchMaster.objects.filter(id=self.location_id ).first()
			self.location_name = branch_id.br_name
			
			if branch_id:
				division_id = branch_id.division_id
				if branch_id.vertical_id:
					vertical_id =branch_id.vertical_id
			if division_id :
				region_id = division_id.region_id
			if region_id:
				vertical_id = region_id.vertical_id


		return {"location_type":self.location_type,"location_name":self.location_name}



def edit_mail_to_bm(request,emp_ins,to_mail):
	"""
		Mail to branch manager with application link and security code to approve/Disapprove employee
	"""

	print("sending mail")
	msub="Employee Edit approve mail"
	mto=to_mail
	mfrom=SYSMAIL
	host = request.get_host()

	url = "http://{host}/edit_employee_approval/{ecode}/".format(host=host,ecode=emp_ins.emp_code)

	mbody="Please click on below link to Approve/Disapprove Employee Update Detail: {url}.".format(url=url)
  
	app_task(args=(msub,mbody,mfrom,mto))
	print("sent")
	return True