from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    headcount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Role(models.Model):
    title = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    salary_band_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_band_max = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("title", "level")

    def __str__(self) -> str:
        return f"{self.title} ({self.level})"


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    hire_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="employees")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="employees")
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    status = models.CharField(max_length=20, choices=(
        ("present", "Present"),
        ("absent", "Absent"),
        ("remote", "Remote"),
        ("leave", "Leave"),
    ))
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("employee", "date")

    def __str__(self) -> str:
        return f"{self.employee} - {self.date} ({self.status})"


class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="performance_reviews")
    period_start = models.DateField()
    period_end = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    goals_met = models.PositiveIntegerField(default=0)
    manager_feedback = models.TextField(blank=True)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "period_start", "period_end")

    def __str__(self) -> str:
        return f"Review {self.employee} {self.period_start} - {self.period_end}"


class Project(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="projects")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Assignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assignments")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="assignments")
    role_on_project = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    allocation_percent = models.PositiveIntegerField(default=100)

    class Meta:
        unique_together = ("employee", "project", "start_date")

    def __str__(self) -> str:
        return f"{self.employee} on {self.project}"
