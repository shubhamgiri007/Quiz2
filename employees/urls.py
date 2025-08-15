from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, RoleViewSet, EmployeeViewSet,
    AttendanceViewSet, PerformanceReviewViewSet, ProjectViewSet, AssignmentViewSet,
    analytics_summary, health, charts, export_employees_csv,
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'performance-reviews', PerformanceReviewViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'assignments', AssignmentViewSet)

urlpatterns = [
    # Place specific paths before router to avoid conflicts with viewset lookups
    path('employees/export.csv', export_employees_csv, name='employees-export'),
    path('analytics/summary/', analytics_summary, name='analytics-summary'),
    path('health/', health, name='health'),
    path('charts/', charts, name='charts'),
    path('', include(router.urls)),
]

