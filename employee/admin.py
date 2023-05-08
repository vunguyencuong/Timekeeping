from django.contrib import admin

# Register your models here.

from employee.models import Employee
from employee.models import Checkin, Query

class EmployeeAdmin(admin.ModelAdmin):
    fieldsets= [
        ('Employee',{'fields': ['name','birthDay','homeTown','phone', 'gender','educationLevel', 'avatar']}),
    ]

class CheckinAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Checkin',{'fields': ['employee', 'date']}),
    ]

class QueryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Query',{'fields': ['avatar']}),
    ]

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Checkin, CheckinAdmin)
admin.site.register(Query, QueryAdmin)