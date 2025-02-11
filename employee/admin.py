from django.contrib import admin
from .models import Employee

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['id', 'last_login', 'date_joined', 'updated_at']
    list_per_page = 10
