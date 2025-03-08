from django.contrib import admin
from .models import Fund, Line, Dept, Item, Employee

# Register your models here.

admin.site.register(Fund)
admin.site.register(Line)
admin.site.register(Dept)
admin.site.register(Item)
admin.site.register(Employee)