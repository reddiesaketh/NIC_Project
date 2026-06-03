from django.urls import path
from .views import (
    # Department
    DepartmentListCreateView,
    DepartmentDetailView,
    # Designation
    DesignationListCreateView,
    DesignationDetailView,
    # Office
    OfficeListCreateView,
    OfficeDetailView,
    # Employee
    EmployeeListCreateView,
    EmployeeDetailView,
    # Employee System
    EmployeeSystemListCreateView,
    EmployeeSystemDetailView,
    EmployeeSystemByEmployeeView,
    # Employee Transfer
    EmployeeTransferListCreateView,
    EmployeeTransferDetailView,
    EmployeeTransferStatusUpdateView,
    EmployeeTransfersByEmployeeView,
    # Dashboard
    DashboardView,
)

app_name = "employees"

urlpatterns = [
    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    # ------------------------------------------------------------------
    # Departments
    # ------------------------------------------------------------------
    path("departments/", DepartmentListCreateView.as_view(), name="department-list-create"),
    path("departments/<int:pk>/", DepartmentDetailView.as_view(), name="department-detail"),

    # ------------------------------------------------------------------
    # Designations
    # ------------------------------------------------------------------
    path("designations/", DesignationListCreateView.as_view(), name="designation-list-create"),
    path("designations/<int:pk>/", DesignationDetailView.as_view(), name="designation-detail"),

    # ------------------------------------------------------------------
    # Offices
    # ------------------------------------------------------------------
    path("offices/", OfficeListCreateView.as_view(), name="office-list-create"),
    path("offices/<int:pk>/", OfficeDetailView.as_view(), name="office-detail"),

    # ------------------------------------------------------------------
    # Employees
    # ------------------------------------------------------------------
    path("employees/", EmployeeListCreateView.as_view(), name="employee-list-create"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),

    # Nested: system details for a specific employee
    path(
        "employees/<int:employee_pk>/system/",
        EmployeeSystemByEmployeeView.as_view(),
        name="employee-system-by-employee",
    ),

    # Nested: all transfers for a specific employee
    path(
        "employees/<int:employee_pk>/transfers/",
        EmployeeTransfersByEmployeeView.as_view(),
        name="employee-transfers-by-employee",
    ),

    # ------------------------------------------------------------------
    # Employee System Details (top-level CRUD)
    # ------------------------------------------------------------------
    path("employee-systems/", EmployeeSystemListCreateView.as_view(), name="employee-system-list-create"),
    path("employee-systems/<int:pk>/", EmployeeSystemDetailView.as_view(), name="employee-system-detail"),

    # ------------------------------------------------------------------
    # Employee Transfers (top-level CRUD + status update)
    # ------------------------------------------------------------------
    path("employee-transfers/", EmployeeTransferListCreateView.as_view(), name="employee-transfer-list-create"),
    path("employee-transfers/<int:pk>/", EmployeeTransferDetailView.as_view(), name="employee-transfer-detail"),
    path(
        "employee-transfers/<int:pk>/status/",
        EmployeeTransferStatusUpdateView.as_view(),
        name="employee-transfer-status-update",
    ),
]
