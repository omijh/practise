# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-31 11:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalancedLeaveMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_code', models.CharField(max_length=45, null=True)),
                ('emp_name', models.CharField(max_length=45, null=True)),
                ('balanced_leave', models.CharField(max_length=45, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CoverageMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coverage', models.CharField(max_length=45, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HolidayListMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday_name', models.CharField(max_length=45, null=True)),
                ('holiday_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('holiday_day', models.CharField(max_length=45)),
                ('coverage', models.CharField(max_length=1000, null=True)),
                ('region', models.CharField(max_length=100, null=True)),
                ('assigned_by', models.CharField(max_length=45, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HolidayTypeMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday_type', models.CharField(max_length=45, null=True)),
                ('short_name_holiday_type', models.CharField(max_length=45, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveAttendanceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(blank=True, max_length=250, null=True)),
                ('action_by', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_name', models.CharField(max_length=45, null=True)),
                ('emp_code', models.CharField(max_length=45, null=True)),
                ('emp_email', models.CharField(max_length=45, null=True)),
                ('leave_status', models.CharField(max_length=45, null=True)),
                ('date_from', models.DateTimeField(null=True)),
                ('date_to', models.DateTimeField(null=True)),
                ('sick_lev_doc_pic', models.FileField(null=True, upload_to='media/doc')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('emp_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='userapp.EmployeeMaster')),
                ('holiday_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='attendanceapp.HolidayTypeMaster')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveTypesMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(max_length=45, null=True)),
                ('short_name_leave_type', models.CharField(max_length=45, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegionMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=45, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StateName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=45, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='leavemaster',
            name='leave_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='attendanceapp.LeaveTypesMaster'),
        ),
        migrations.AddField(
            model_name='leaveattendancelog',
            name='lev_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='attendanceapp.LeaveMaster'),
        ),
        migrations.AddField(
            model_name='holidaylistmaster',
            name='holiday_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='attendanceapp.HolidayTypeMaster'),
        ),
        migrations.AddField(
            model_name='holidaylistmaster',
            name='state_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='attendanceapp.StateName'),
        ),
        migrations.AddField(
            model_name='coveragemaster',
            name='state_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='attendanceapp.StateName'),
        ),
        migrations.AddField(
            model_name='balancedleavemaster',
            name='balanced_leave_type_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='attendanceapp.LeaveTypesMaster'),
        ),
    ]
