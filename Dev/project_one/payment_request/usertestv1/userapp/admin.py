from django.contrib import admin

# Register your models here.

from .models import VerticalMaster,RegionMaster,DivisionMaster,BranchMaster, AppApproverMaster

class VerticalMasterAdmin(admin.ModelAdmin):
    list_display = ('id','vt_name','manager_name','manager_email','manager_code',)
    list_display_links = ('id',)
   
    search_fields = ('vt_name','manager_name')
    list_per_page = 50


admin.site.register(VerticalMaster,VerticalMasterAdmin)



class RegionMasterAdmin(admin.ModelAdmin):
    list_display = ('id','manager_name','manager_email','manager_code','vertical_id')
    list_display_links = ('vertical_id',)
   
    search_fields = ('rg_name','manager_name')
    list_per_page = 50


admin.site.register(RegionMaster,RegionMasterAdmin)


class DivisionMasterAdmin(admin.ModelAdmin):
    list_display = ('id','div_name','manager_name','manager_email','manager_code','vertical_id','region_id')
    list_display_links = ('id',)
   
    search_fields = ('div_name','manager_name')
    list_per_page = 50


admin.site.register(DivisionMaster,DivisionMasterAdmin)





class BranchMasterAdmin(admin.ModelAdmin):
    list_display = ('id','br_name','manager_name','manager_email','manager_code','vertical_id','region_id','division_id','cfo_name','cfo_email')
    list_display_links = ('id',)
   
    search_fields = ('br_name','manager_name')
    list_per_page = 50


admin.site.register(BranchMaster,BranchMasterAdmin)



class AppApproverMasterAdmin(admin.ModelAdmin):
    list_display = ('app_id','approver_level','approver_name','approver_email','status')
    list_display_links = ('app_id',)
   
    search_fields = ('app_id','approver_name')
    list_per_page = 50


admin.site.register(AppApproverMaster,AppApproverMasterAdmin)



