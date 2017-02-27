from django.contrib import admin

# Register your models here.
from .models import Employee,Leave

admin.site.register(Employee)
admin.site.register(Leave)
