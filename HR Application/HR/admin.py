from django.contrib import admin
from .models import User, Employee, RequestedLeaves

# admin access created
admin.site.register(Employee)
admin.site.register(RequestedLeaves)
