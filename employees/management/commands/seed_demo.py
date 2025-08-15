from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from random import randint, choice, uniform
from datetime import date, timedelta

from employees.models import Department, Role, Employee, Attendance, PerformanceReview, Project, Assignment


class Command(BaseCommand):
    help = 'Seed the database with demo data (4-5 employees and related records)'

    def add_arguments(self, parser):
        parser.add_argument('--employees', type=int, default=5, help='Number of employees to create')

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker()

        # Departments
        departments = []
        for code, name in [("ENG", "Engineering"), ("HR", "Human Resources"), ("FIN", "Finance")]:
            dept, _ = Department.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'budget': randint(100000, 1000000),
                    'headcount': 0,
                }
            )
            departments.append(dept)

        # Roles
        roles = []
        role_defs = [
            ("Software Engineer", "L1", 50000, 80000),
            ("Software Engineer", "L2", 80000, 120000),
            ("Manager", "M1", 90000, 140000),
            ("HR Generalist", "L1", 40000, 70000),
        ]
        for title, level, smin, smax in role_defs:
            role, _ = Role.objects.get_or_create(
                title=title, level=level,
                defaults={'salary_band_min': smin, 'salary_band_max': smax}
            )
            roles.append(role)

        # Projects
        projects = []
        for i in range(3):
            dept = choice(departments)
            project, _ = Project.objects.get_or_create(
                code=f"PRJ{i+1:03d}",
                defaults={
                    'name': f"Project {i+1}",
                    'department': dept,
                    'start_date': date.today() - timedelta(days=randint(30, 180)),
                    'budget': randint(20000, 200000),
                }
            )
            projects.append(project)

        # Employees
        num_employees = options['employees']
        employees = []
        for _ in range(num_employees):
            dept = choice(departments)
            role = choice(roles)
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
            employee = Employee.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                hire_date=date.today() - timedelta(days=randint(100, 2000)),
                department=dept,
                role=role,
                base_salary=randint(int(role.salary_band_min), int(role.salary_band_max)),
                is_active=True,
            )
            employees.append(employee)

        # Update headcount
        for dept in departments:
            dept.headcount = dept.employees.count()
            dept.save(update_fields=['headcount'])

        # Attendance and Reviews
        for emp in employees:
            # Assign to a project
            proj = choice(projects)
            Assignment.objects.get_or_create(
                employee=emp,
                project=proj,
                start_date=emp.hire_date + timedelta(days=randint(0, 30)),
                defaults={
                    'role_on_project': choice(["Developer", "QA", "Lead", "Analyst"]),
                    'allocation_percent': choice([50, 75, 100]),
                }
            )

            # Create last 30 days attendance
            for i in range(30):
                d = date.today() - timedelta(days=i)
                status = choice(["present", "present", "present", "remote", "leave", "absent"])  # bias to present
                hours = 0 if status in ("leave", "absent") else round(uniform(6, 9), 2)
                Attendance.objects.update_or_create(
                    employee=emp,
                    date=d,
                    defaults={'status': status, 'hours_worked': hours}
                )

            # Two performance reviews
            for j in range(2):
                end = date.today() - timedelta(days=90 * j)
                start = end - timedelta(days=90)
                PerformanceReview.objects.update_or_create(
                    employee=emp,
                    period_start=start,
                    period_end=end,
                    defaults={
                        'rating': round(uniform(2.5, 5.0), 1),
                        'goals_met': randint(3, 10),
                        'manager_feedback': fake.sentence(nb_words=12),
                        'bonus_amount': round(uniform(500, 5000), 2),
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"Seeded demo data with {num_employees} employees."))


