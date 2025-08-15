from django.contrib import admin
from .models import Department, Role, Employee, Attendance, PerformanceReview, Project, Assignment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "budget", "headcount")
    search_fields = ("code", "name")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "salary_band_min", "salary_band_max")
    search_fields = ("title", "level")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "department", "role", "hire_date", "is_active")
    list_filter = ("department", "role", "is_active")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "status", "hours_worked")
    list_filter = ("status",)
    search_fields = ("employee__first_name", "employee__last_name", "employee__email")


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ("employee", "period_start", "period_end", "rating", "bonus_amount")
    list_filter = ("rating",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department", "start_date", "end_date", "budget")
    list_filter = ("department",)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("employee", "project", "role_on_project", "start_date", "end_date", "allocation_percent")
    list_filter = ("project",)

# Register your models here.
