from django.contrib import admin
from .models import Fund, Line, Dept, Item, Employee, People, Invoice,PurchaseOrder,Voucher,ActivityList, Payroll, PayPeriod, Grant, GrantAllocation, BudgetActions, Carryover, Benefits, Variable, Clockify, Testing


class GrantAllocationInline(admin.TabularInline):
    model = GrantAllocation
    extra = 1

class GrantAdmin(admin.ModelAdmin):
    list_display = ("grant_id", "grant_name")
    inlines = [GrantAllocationInline]
# Register your models here.

admin.site.register(Fund)
admin.site.register(Line)
admin.site.register(Dept)
admin.site.register(Item)
admin.site.register(Employee)
admin.site.register(People)
admin.site.register(Invoice)
admin.site.register(PurchaseOrder)
admin.site.register(Voucher)
admin.site.register(ActivityList)
admin.site.register(Payroll)
admin.site.register(PayPeriod)
admin.site.register(Grant, GrantAdmin)
admin.site.register(BudgetActions)
admin.site.register(Carryover)
admin.site.register(Benefits)
admin.site.register(Variable)
admin.site.register(Clockify)



admin.site.register(Testing)