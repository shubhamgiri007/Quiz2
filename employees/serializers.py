from rest_framework import serializers
from .models import Department, Role, Employee, Attendance, PerformanceReview, Project, Assignment


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department', write_only=True)
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'email', 'hire_date', 'base_salary', 'is_active',
            'department', 'department_id', 'role', 'role_id', 'created_at', 'updated_at'
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class EmployeeSummarySerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    department = serializers.CharField()
    role = serializers.CharField()
    average_rating = serializers.FloatField()
    total_bonus = serializers.FloatField()
    attendance_present_days = serializers.IntegerField()

