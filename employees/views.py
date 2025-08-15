from django.db.models import Avg, Sum, Count, Q
from django.shortcuts import render
import json
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle
from .models import Department, Role, Employee, Attendance, PerformanceReview, Project, Assignment
from .serializers import (
    DepartmentSerializer,
    RoleSerializer,
    EmployeeSerializer,
    AttendanceSerializer,
    PerformanceReviewSerializer,
    ProjectSerializer,
    AssignmentSerializer,
    EmployeeSummarySerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 500


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('id')
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'budget', 'headcount']


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'level']
    ordering_fields = ['title', 'level', 'salary_band_min', 'salary_band_max']


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department', 'role').all().order_by('id')
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'department__name', 'role__title']
    ordering_fields = ['hire_date', 'base_salary']
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['department', 'role', 'is_active']

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        employee = self.get_object()
        reviews = PerformanceReview.objects.filter(employee=employee)
        attendance = Attendance.objects.filter(employee=employee)
        data = {
            'employee_id': employee.id,
            'employee_name': f"{employee.first_name} {employee.last_name}",
            'department': employee.department.name,
            'role': f"{employee.role.title} ({employee.role.level})",
            'average_rating': reviews.aggregate(r=Avg('rating'))['r'] or 0.0,
            'total_bonus': float(reviews.aggregate(b=Sum('bonus_amount'))['b'] or 0),
            'attendance_present_days': attendance.filter(status='present').count(),
        }
        return Response(EmployeeSummarySerializer(data).data)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee').all().order_by('-date')
    serializer_class = AttendanceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['employee__first_name', 'employee__last_name', 'status']
    ordering_fields = ['date', 'hours_worked']
    filterset_fields = ['status', 'date', 'employee']


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.select_related('employee').all().order_by('-period_end')
    serializer_class = PerformanceReviewSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['employee__first_name', 'employee__last_name']
    ordering_fields = ['rating', 'bonus_amount', 'period_end']
    filterset_fields = ['employee', 'period_start', 'period_end']


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('department').all().order_by('start_date')
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'department__name']
    ordering_fields = ['start_date', 'end_date', 'budget']
    filterset_fields = ['department']


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('employee', 'project').all().order_by('start_date')
    serializer_class = AssignmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['employee__first_name', 'employee__last_name', 'project__name']
    ordering_fields = ['start_date', 'end_date', 'allocation_percent']
    filterset_fields = ['employee', 'project']


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_summary(request):
    # Aggregate summaries across employees
    avg_rating = PerformanceReview.objects.aggregate(v=Avg('rating'))['v'] or 0
    total_bonus = PerformanceReview.objects.aggregate(v=Sum('bonus_amount'))['v'] or 0
    headcount_by_dept = Department.objects.annotate(c=Count('employees')).values('name', 'c').order_by('name')

    return Response({
        'average_rating_overall': float(avg_rating),
        'total_bonus_paid': float(total_bonus),
        'headcount_by_department': list(headcount_by_dept),
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health(request):
    return Response({'status': 'ok'})


def charts(request):
    headcount_by_dept = Department.objects.annotate(c=Count('employees')).values_list('name', 'c').order_by('name')
    avg_ratings = (
        PerformanceReview.objects.values('employee__first_name', 'employee__last_name')
        .annotate(avg=Avg('rating'))
        .order_by('-avg')[:10]
    )
    labels = [name for name, _ in headcount_by_dept]
    counts = [count for _, count in headcount_by_dept]
    emp_labels = [f"{r['employee__first_name']} {r['employee__last_name']}" for r in avg_ratings]
    emp_values = [float(r['avg'] or 0) for r in avg_ratings]
    context = {
        'dept_labels_json': json.dumps(labels),
        'dept_counts_json': json.dumps(counts),
        'emp_labels_json': json.dumps(emp_labels),
        'emp_values_json': json.dumps(emp_values),
    }
    return render(request, 'employees/charts.html', context)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def export_employees_csv(request):
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Hire Date', 'Department', 'Role', 'Base Salary', 'Active'])
    for e in Employee.objects.select_related('department', 'role').all():
        writer.writerow([e.id, e.first_name, e.last_name, e.email, e.hire_date, e.department.name, f"{e.role.title} {e.role.level}", e.base_salary, e.is_active])

    return response

# Create your views here.
