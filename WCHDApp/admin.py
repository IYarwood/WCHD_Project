from django.contrib import admin
from .models import Fund, Line, Dept, Item, Employee, People, Invoice,PurchaseOrder,Voucher,ActivityList, Payroll, PayPeriod, Grant, GrantAllocation, BudgetActions, Carryover, Benefits, Variable, Clockify, Testing, GrantLine, Expense, GrantExpense


class PeopleAdmin(admin.ModelAdmin):
    search_fields = ['name']

class ExpenseAdmin(admin.ModelAdmin):
    autocomplete_fields = ['people']

class GrantAdmin(admin.ModelAdmin):
    list_display = ("grant_id", "grant_name")
# Register your models here.

admin.site.register(Fund)
admin.site.register(Line)
admin.site.register(Dept)
admin.site.register(Item)
admin.site.register(Employee)
admin.site.register(People, PeopleAdmin)
admin.site.register(Invoice)
admin.site.register(PurchaseOrder)
admin.site.register(Voucher)
admin.site.register(ActivityList)
admin.site.register(Payroll)
admin.site.register(PayPeriod)
admin.site.register(Grant, GrantAdmin)
admin.site.register(GrantLine)
admin.site.register(BudgetActions)
admin.site.register(Carryover)
admin.site.register(Benefits)
admin.site.register(Variable)
admin.site.register(Clockify)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(GrantExpense)



admin.site.register(Testing)