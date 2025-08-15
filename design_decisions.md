## Architecture & Design Decisions

### Tech Stack
- Django 4.2 LTS and Django REST Framework for rapid development and robust ORM.
- SimpleJWT for stateless auth.
- drf-yasg for interactive Swagger UI.
- PostgreSQL via `DATABASE_URL` with `dj-database-url`. Default to SQLite for quick local run.
- Faker for synthetic data seeding.

### Domain Modeling
- Core entities: `Department`, `Role`, `Employee`, `Attendance`, `PerformanceReview`, `Project`, `Assignment`.
- Relationships:
  - Employee belongs to a Department and Role.
  - Attendance and PerformanceReview belong to Employee.
  - Project belongs to Department; Assignment links Employee to Project with allocation and dates.
- Rationale: Covers HR and performance analytics with minimal, normalized schema.

### APIs
- CRUD for all core models via DRF `ModelViewSet` and router.
- Analytics endpoint aggregates avg rating, total bonus, and headcount per department.
- Per-employee summary action provides key KPIs for a person.
- Pagination, ordering, search, and basic filter fields enabled.
- Throttling applied globally using DRF settings.

### Auth
- JWT access/refresh tokens to secure APIs; open `/health/` for Kubernetes-style probes.

### Visualization
- Simple `charts.html` page using Chart.js to render headcount and top-rated employees.
- Optional and decoupled from API contract.

### Data Generation
- Management command `seed_demo` creates departments, roles, projects, 4-5 employees with 30 days of attendance and two reviews.

### Performance Notes
- Use `select_related` on frequently joined relations.
- Router endpoints with pagination default to 20 items, max 500 per page.
- For bonus constraints (not hard-enforced): iterate over employees in batches when exporting; current export streams rows to response without loading everything into memory.

### Trade-offs
- Default to SQLite to ensure the project runs quickly without external deps; switch to PostgreSQL by setting `DATABASE_URL`.
- Minimal tests due to time constraints; prioritized working features and documentation.


