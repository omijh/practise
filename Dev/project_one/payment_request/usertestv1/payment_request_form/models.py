# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from userapp.models import EmployeeMaster,BranchMaster,DivisionMaster,DesignationMaster,AppMaster,EmpAppDetail,AppRole,AppAdmin
# Create your models here.

# form to use the payment same as google form
states = (
	('NEW', 'New'),
	('APR','Approve'),
	('DEC','Decline'),
	('PSD','Processed')
	)
class PaymentMaster(models.Model):
	
	branch_name = models.ForeignKey('userapp.BranchMaster', models.DO_NOTHING,null=True)
	nature_of_expenses =  models.CharField(max_length=50,blank=True,null=True)
	dept_name = models.ForeignKey('userapp.DesignationMaster', models.DO_NOTHING,null=True)
	amount = models.FloatField(default=0.0)
	bank_acc_no = models.IntegerField(blank=True,null=True)
	ifsc_code = models.CharField(max_length=50,blank=True,null=True)
	head_of_accounts = models.ForeignKey('HeadOfAccounts',models.DO_NOTHING,null=True)
	gl_code =  models.IntegerField(blank=True,null=True)
	gl_desc = models.CharField(max_length=50,blank=True,null=True)
	status = models.CharField(max_length=3,choices=states,default='NEW')
	invoice_number = models.CharField(max_length=50,blank=True,null=True)
	approve_lvl = models.BooleanField(default=False)
	approval_date_lvl1 = models.DateField(null=True,blank=True)
	bm_email = models.CharField(max_length=50,blank=True,null=True)
	approve_lvl2 = models.BooleanField(default=False)
	approval_date_lvl2 = models.DateField(null=True,blank=True)
	dm_email = models.CharField(max_length=50,blank=True,null=True)
	approve_lvl3 = models.BooleanField(default=False)
	approval_date_lvl3 = models.DateField(null=True,blank=True)
	approve_lvl4 = models.BooleanField(default=False)
	approval_date_lvl4 = models.DateField(null=True,blank=True)
	rm_email = models.CharField(max_length=50,blank=True,null=True)
	cfo_email = models.CharField(max_length=50,blank=True,null=True)
	payment_date = models.DateField()
	name_of_party = models.CharField(max_length=50,blank=True,null=True)
	name_of_bank = models.CharField(max_length=50,blank=True,null=True)
	document = models.FileField(upload_to='documents/%Y/%m/%d/',null=True)

	def __str__(self):
  	  return 'ID={0}, Status={1}, Amount={2}'.format(self.id, self.status,self.amount)


class HeadOfAccounts(models.Model):
	name = models.CharField(max_length=50,null=False)
	gl_code =  models.IntegerField(blank=True,null=True)
	gl_desc =  models.CharField(max_length=50,blank=True,null=True)

	def __str__(self):
  	  return '{0},{1}'.format(self.name, self.gl_code)

# class UploadCSV(models.Model):
# 	csv_doc = models.FileField(upload_to='csv_doc/%Y/%m/%d/',null=True)

# class GLMaster(models.Model):
# 	gl_code =  models.IntegerField(blank=True,null=True)
# 	gl_desc =  models.CharField(max_length=50,blank=True,null=True)

# 	def __str__(self):
# 		return self.gl_desc