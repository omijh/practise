# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import sys
import datetime
from django import template
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from user_management.logger import log
from string import Template
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import * 
from userapp.models import EmployeeMaster,BranchMaster,DivisionMaster,DesignationMaster,AppMaster,EmpAppDetail,AppRole,AppAdmin,RegionMaster
from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.contrib  import messages
from django.template.loader import render_to_string
from payment_request_form.models import PaymentMaster
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import csv
import threading

def upload_ack(request):
	bad_ids = []
	if request.FILES:
		csv_doc = request.FILES['csv_doc']
		if csv_doc:
			filename = csv_doc.name
			if filename.endswith('.csv'):
				decoded_file = csv_doc.read().decode('utf-8').splitlines()
				reader = csv.reader(decoded_file)
				for index,row in enumerate(reader):
					if index > 0:
						request_id = row[0][2:]
						pay_ins = PaymentMaster.objects.filter(pk=int(request_id)).first()
						if not pay_ins:
							bad_ids.append(row[0])
						else:
							if pay_ins.status != 'APR':
								bad_ids.append(row[0])
							if not row[15] or not row[16]:
								bad_ids.append(row[0])
				if not bad_ids:
					if index > 0:
						request_id = row[0][2:]
						pay_ins = PaymentMaster.objects.filter(pk=int(request_id)).first()
						if pay_ins:
							if pay_ins.status == 'APR' and row[15] and row[16]:
								msub="Vendor payment request: "+str(pay_ins.invoice_number)
								mfrom=""
								mto=pay_ins.bm_email
								dmto = pay_ins.dm_email
								rmto = pay_ins.rm_email
								cfo_email = pay_ins.cfo_email
								url = request.build_absolute_uri()
								rest_url = request.get_full_path()
								final_url = url.replace(rest_url,'')
								context = {
									'invoice_number':pay_ins.invoice_number,
									'processed_date':row[15]
								}
								mbody = render_to_string('payment_request_form/corp_email.html',context)
								if mto:
									EmailThread(msub,mbody,mfrom,mto).start()
								if dmto:
									EmailThread(msub,mbody,mfrom,dmto).start()
								if rmto:
									EmailThread(msub,mbody,mfrom,rmto).start()
								if cfo_email:
									EmailThread(msub,mbody,mfrom,cfo_email).start()
								PaymentMaster.objects.filter(pk=int(request_id)).update(status='PSD')
				else:
					context = {'messageids': bad_ids}
					return render(request, 'payment_request_form/update_ack.html', context)						
			else:
				context = {'message': 'FormatError'}
				return render(request, 'payment_request_form/update_ack.html', context)
	context = {
	}
	return render(request, 'payment_request_form/update_ack.html',context)

class EmailThread(threading.Thread):
	def __init__(self,msub,mbody,mfrom,mto,attachment= None):
		self.msub = msub
		self.mbody = mbody
		self.mfrom = mfrom
		self.mto = mto
		self.attachment = attachment
		threading.Thread.__init__(self)

	def run(self):
		text_content = 'This is an important message.'
		msg = EmailMultiAlternatives(self.msub, text_content, self.mfrom, [self.mto])
		if self.attachment:
			msg.attach_file(self.attachment)
		msg.attach_alternative(self.mbody, "text/html")
		msg.send()
		return True

def export_payment_form(request):
	if request.method == 'POST':
		date_from = request.POST.get('payment_date_from',None)
		date_to = request.POST.get('payment_date_to',None)
		d1 = datetime.strptime(date_from, '%Y-%m-%d').date()
		date_from = datetime.combine(d1, datetime.min.time())
		d2 = datetime.strptime(date_to, '%Y-%m-%d').date()
		date_to = datetime.combine(d2, datetime.min.time())
		# apr_sel = request.POST.get('apv_sel',None)
		payment_ins = PaymentMaster.objects.filter(payment_date__range=[date_from, date_to],status="APR")
		# payment_ins = PaymentMaster.objects.filter(payment_date__range=[date_from, date_to],status="APR") if apr_sel =='aprov' else PaymentMaster.objects.filter(payment_date__range=[date_from, date_to])
		nature_of_expenses =[]
		branch_name = BranchMaster.objects.all()
		dept_name = DesignationMaster.objects.all()
		head_of_accounts = HeadOfAccounts.objects.all()
		context = {
		'nature_of_expenses': nature_of_expenses,
		'branch_name' : branch_name,
		'dept_name':dept_name,
		'head_of_accounts':head_of_accounts,
		'payment_request':payment_ins,
		'date_from':d1,
		'date_to':d2,
		}
		return render(request, 'payment_request_form/export_payment.html',context)

def export_csv(request,datefrom=None,dateto=None):
		date_from = datefrom
		date_to = dateto
		d1 = datetime.strptime(date_from, '%Y-%m-%d').date()
		date_from = datetime.combine(d1, datetime.min.time())
		d2 = datetime.strptime(date_to, '%Y-%m-%d').date()
		date_to = datetime.combine(d2, datetime.min.time())
		# apr_sel = apr
		payment_ins = PaymentMaster.objects.filter(payment_date__range=[date_from, date_to],status="APR")
		# payment_ins = PaymentMaster.objects.filter(payment_date__range=[date_from, date_to],status="APR") if apr_sel =='aprov' else PaymentMaster.objects.filter(payment_date__range=[date_from, date_to])
		nature_of_expenses =[]
		branch_name = BranchMaster.objects.all()
		dept_name = DesignationMaster.objects.all()
		head_of_accounts = HeadOfAccounts.objects.all()

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="payment_request.csv"'

		writer = csv.writer(response)
		writer.writerow(['Request ID','Date', 'Branch Name', 'Head of Accounts', 'Narration / Nature of Expenses','Department / Cost Centre','Invoice Number','Date','Amount','NAME OF THE PARTY','NAME OF BANK','BANK A/C NO','IFSC CODE','GL Code','GL Description','Payment Processed Date','Status'])
		for forms in payment_ins:
			req_id = 'RI'+str(forms.id)
			writer.writerow([req_id,forms.payment_date, forms.branch_name.br_name, forms.head_of_accounts.name, forms.nature_of_expenses,forms.dept_name.desg_name,forms.invoice_number,forms.payment_date,forms.amount,forms.name_of_party,forms.name_of_bank,forms.bank_acc_no,forms.ifsc_code,forms.gl_code,forms.gl_desc,'',''])
		return response

def export_payment_request(request):
	try:
		log.debug("Entering try block")
		nature_of_expenses =[]
		branch_name = BranchMaster.objects.all()
		dept_name = DesignationMaster.objects.all()
		head_of_accounts = HeadOfAccounts.objects.all()
		context = {
		'nature_of_expenses': nature_of_expenses,
		'branch_name' : branch_name,
		'dept_name':dept_name,
		'head_of_accounts':head_of_accounts,
		'payment_request':[],
		}
		return render(request, 'payment_request_form/export_payment.html',context)
	except Exception as e: 
		log.exception(e)
		return redirect('index')

def approve(request,des,id=None):
	if id:
		payment_ins = payment_obj = PaymentMaster.objects.filter(pk=id).first()
		apr_email = payment_obj.branch_name.manager_email
		apr2_email = payment_obj.branch_name.division_id.manager_email
		apr3_email = payment_obj.branch_name.region_id.manager_email
		apr4_email = payment_obj.branch_name.cfo_email
		if des == 'b':
			PaymentMaster.objects.filter(pk=id).update(approve_lvl=True,approval_date_lvl1=datetime.now(),bm_email=apr_email)
		elif des == 'd':
			PaymentMaster.objects.filter(pk=id).update(approve_lvl2=True,approval_date_lvl2=datetime.now(),dm_email=apr2_email)
		elif des == 'r':
			PaymentMaster.objects.filter(pk=id).update(approve_lvl3=True,approval_date_lvl3=datetime.now(),rm_email=apr3_email)
		elif des == 'c':
			PaymentMaster.objects.filter(pk=id).update(approve_lvl4=True,approval_date_lvl4=datetime.now(),cfo_email=apr4_email)
		payment_ins = payment_obj = PaymentMaster.objects.filter(pk=id).first()
		amount = payment_obj.amount
		apr = payment_obj.approve_lvl
		apr2 = payment_obj.approve_lvl2
		apr3 = payment_obj.approve_lvl3
		apr4 = payment_obj.approve_lvl4
		msub="Vendor payment request"
		mfrom=""
		mto=payment_ins.branch_name.manager_email
		dmto = payment_ins.branch_name.division_id.manager_email
		rmto = payment_ins.branch_name.region_id.manager_email
		cfo_email = payment_ins.branch_name.cfo_email
		url = request.build_absolute_uri()
		rest_url = request.get_full_path()
		final_url = url.replace(rest_url,'')
		context_dm = {
			'amount':amount,
			'user':request.user.username,
			'branch_name':payment_ins.branch_name.br_name,
			'bank_acc_no':payment_ins.bank_acc_no,
			'head_of_accounts':payment_ins.head_of_accounts.name,
			'designation':payment_ins.dept_name.desg_name,
			'manager_name':payment_ins.branch_name.division_id.manager_name,
			'nature_of_expenses':payment_ins.nature_of_expenses,
			'approval_url': str(final_url)+'/'+'payment_request'+'/'+'d'+'/'+str(payment_ins.pk)+'/'+'approve',
			'deny_url':str(final_url)+'/'+'payment_request'+'/'+'d'+'/'+str(payment_ins.pk)+'/'+'decline',
			
		}
		context_rm = {
			'amount':amount,
			'user':request.user.username,
			'branch_name':payment_ins.branch_name.br_name,
			'bank_acc_no':payment_ins.bank_acc_no,
			'manager_name':payment_ins.branch_name.region_id.manager_name,
			'head_of_accounts':payment_ins.head_of_accounts.name,
			'designation':payment_ins.dept_name.desg_name,
			'nature_of_expenses':payment_ins.nature_of_expenses,
			'approval_url': str(final_url)+'/'+'payment_request'+'/'+'r'+'/'+str(payment_ins.pk)+'/'+'approve',
			'deny_url':str(final_url)+'/'+'payment_request'+'/'+'r'+'/'+str(payment_ins.pk)+'/'+'decline',
		}
		context_cfo = {
			'amount':amount,
			'user':request.user.username,
			'branch_name':payment_ins.branch_name.br_name,
			'bank_acc_no':payment_ins.bank_acc_no,
			'manager_name':payment_ins.branch_name.cfo_name,
			'head_of_accounts':payment_ins.head_of_accounts.name,
			'designation':payment_ins.dept_name.desg_name,
			'nature_of_expenses':payment_ins.nature_of_expenses,
			'approval_url': str(final_url)+'/'+'payment_request'+'/'+'c'+'/'+str(payment_ins.pk)+'/'+'approve',
			'deny_url':str(final_url)+'/'+'payment_request'+'/'+'c'+'/'+str(payment_ins.pk)+'/'+'decline',
		}
		dmbody = render_to_string('payment_request_form/email.html',context_dm)
		rmbody = render_to_string('payment_request_form/email.html',context_rm)
		cfombody = render_to_string('payment_request_form/email.html',context_cfo)

		if amount <= 25000:
			if apr:
				PaymentMaster.objects.filter(pk=id).update(status='APR')
		elif amount > 25000 and amount <= 50000:
			if apr and apr2:
				PaymentMaster.objects.filter(pk=id).update(status='APR')
			elif not apr2 and apr:
				EmailThread(msub,dmbody,mfrom,dmto,payment_ins.document.path).start()
		elif amount > 50000 and amount <= 100000:
			if apr and apr2 and apr3:
				PaymentMaster.objects.filter(pk=id).update(status='APR')
			elif not apr2 and apr:
				EmailThread(msub,dmbody,mfrom,dmto,payment_ins.document.path).start()
			elif not apr3 and apr and apr2:
				EmailThread(msub,rmbody,mfrom,rmto,payment_ins.document.path).start()
		elif amount > 100000:
			if apr and apr2 and apr3 and apr4:
				PaymentMaster.objects.filter(pk=id).update(status='APR')
			elif not apr2 and apr:
				EmailThread(msub,dmbody,mfrom,dmto,payment_ins.document.path).start()
			elif not apr3 and apr and apr2:
				EmailThread(msub,rmbody,mfrom,rmto,payment_ins.document.path).start()
			elif not apr4 and apr and apr2 and apr3:
				EmailThread(msub,cfombody,mfrom,cfo_email).start()
		messages.success(request, "Successfully approved")
	return HttpResponse('<script type="text/javascript">window.close()</script>')
	
def decline(request,des,id=None):
	if id:
		PaymentMaster.objects.filter(pk=id).update(status='DEC')
		messages.success(request, "Successfully declined")
	return HttpResponse('<script type="text/javascript">window.close()</script>')  

def payment_request(request):
	try:
		log.debug("Entering try block")		
		nature_of_expenses =[]
		branch_name = BranchMaster.objects.all()
		dept_name = DesignationMaster.objects.all()
		head_of_accounts = HeadOfAccounts.objects.all()
		context = {
		'nature_of_expenses': nature_of_expenses,
		'branch_name' : branch_name,
		'dept_name':dept_name,
		'head_of_accounts':head_of_accounts,
		}
		return render(request, 'payment_request_form/payment_form.html',context)
	except Exception as e: 
		log.exception(e)
		return redirect('index')


def drop_down_list(request):
	"""
	drop down lists for Vertical, Region, Division, Branch using ajax
	"""
	try:
		log.debug("Entering try block")

		log.info("In test app .....................................")
		selected_id = request.GET.get('data_id')
		drop_down_type = request.GET.get('type')
		selected_hoa = request.GET.get('data_hoa')
		data={}
		
		if drop_down_type=="branch_list":
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

		if drop_down_type=="head_list":
			head_list = HeadOfAccounts.objects.filter(id= selected_id).first()
			if head_list:

				data={
				"gl_code":head_list.gl_code,
				"gl_desc":head_list.gl_desc,
				}
					
				return JsonResponse(data)
	except Exception as e:
		log.exception(e)
		return redirect('index')





def save_payment_form(request):

	if request.method == 'POST' and request.FILES['document']:
			
		branch_name = request.POST.getlist('branch_name',None)
		dept_name = request.POST.getlist('dept_name') or None
		division = request.POST.getlist('division') or None
		region = request.POST.getlist('region') or None
		amount = request.POST.get('amount',None)
		bank_acc_no = request.POST.get('bank_acc_no',None)
		ifsc_code = request.POST.get('ifsc_code',None)
		name_of_party = request.POST.get('name_of_party',None)
		name_of_bank = request.POST.get('name_of_bank',None)
		invoice_number = request.POST.get('invoice_number',None)
		# pay_date_str = request.POST.get('date',None)
		nature_of_expenses=request.POST.get('nature_of_expenses',None)
		head_of_accounts=request.POST.get('head_of_accounts',None)
		pay_date_str = request.POST.get('payment_date',None)
		gl_code = request.POST.get('gl_code',None)
		gl_desc = request.POST.get('gl_desc',None)
		document = request.FILES['document']
		fs = FileSystemStorage()
		filename = fs.save(document.name, document)
		if branch_name  :
			if not branch_name[0] in [str("None"),""] : 
				branch_ins = BranchMaster.objects.filter(id=branch_name[0]).first()

		if region  :
			if not region[0] in [str("None"),""] : 
				region_ins = RegionMaster.objects.filter(id=region[0]).first()

		if division  :
			if not division[0] in [str("None"),""] : 
				division_ins = DivisionMaster.objects.filter(id=division[0]).first()

		if dept_name  :
			if not dept_name[0] in [str("None"),""] : 
				dep_ins = DesignationMaster.objects.filter(id=dept_name[0]).first()
		if head_of_accounts:
			if not head_of_accounts[0] in [str("None"),""] : 
				hoa_ins = HeadOfAccounts.objects.filter(id=head_of_accounts[0]).first()

		pay_date = parse_date(pay_date_str)
		amount=float(amount)
		payment_ins=PaymentMaster()
		payment_ins.branch_name=branch_ins
		payment_ins.nature_of_expenses = nature_of_expenses
		payment_ins.dept_name  = dep_ins
		payment_ins.amount = amount
		payment_ins.bank_acc_no = bank_acc_no
		payment_ins.ifsc_code = ifsc_code
		payment_ins.head_of_accounts = hoa_ins
		payment_ins.payment_date = pay_date
		payment_ins.invoice_number = invoice_number
		payment_ins.name_of_party = name_of_party
		payment_ins.name_of_bank = name_of_bank
		payment_ins.gl_desc = hoa_ins.gl_desc
		payment_ins.gl_code = hoa_ins.gl_code
		payment_ins.document = document
		payment_ins.save()

		if payment_ins.pk is not None:
			msub="Vendor payment request"
			mfrom=""
			mto=payment_ins.branch_name.manager_email
			dmto = payment_ins.branch_name.division_id.manager_email
			rmto = payment_ins.branch_name.region_id.manager_email
			url = request.build_absolute_uri()
			rest_url = request.get_full_path()
			final_url = url.replace(rest_url,'')
			context = {
				'amount':amount,
				'user':request.user.username,
				'branch_name':branch_ins.br_name,
				'bank_acc_no':bank_acc_no,
				'head_of_accounts':hoa_ins.name,
				'manager_name':payment_ins.branch_name.manager_name,
				'designation':payment_ins.dept_name.desg_name,
				'nature_of_expenses':payment_ins.nature_of_expenses,
				'name_of_party': payment_ins.name_of_party,
				'approval_url': str(final_url)+'/'+'payment_request'+'/'+'b'+'/'+str(payment_ins.pk)+'/'+'approve',
				'deny_url':str(final_url)+'/'+'payment_request'+'/'+'b'+'/'+str(payment_ins.pk)+'/'+'decline',
			}
			mbody = render_to_string('payment_request_form/email.html',context)
			EmailThread(msub,mbody,mfrom,mto,payment_ins.document.path).start()
			context = {'message': 'Success'}
			return render(request, 'payment_request_form/payment_form.html', context)
		else:
			context = {'message': 'Fail'}
			return render(request, 'payment_request_form/payment_form.html', context)