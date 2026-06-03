from django.contrib import admin
from .models import (
    Department,
    Designation,
    Office,
    Employee,
    EmployeeSystem,
    EmployeeTransfer,
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "code"]
    ordering = ["name"]


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "code"]
    ordering = ["name"]


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "office_type", "district", "is_active", "created_at"]
    list_filter = ["is_active", "office_type", "district__state"]
    search_fields = ["name", "code", "district__name"]
    raw_id_fields = ["district", "created_by"]
    ordering = ["name"]


class EmployeeSystemInline(admin.StackedInline):
    model = EmployeeSystem
    extra = 0
    fields = [
        "computer_name",
        "ip_address",
        "mac_address",
        "operating_system",
        "os_version",
        "domain_username",
        "assigned_at",
        "is_active",
    ]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "employee_id",
        "full_name",
        "office",
        "department",
        "designation",
        "employment_status",
        "employment_type",
        "is_active",
        "date_of_joining",
    ]
    list_filter = [
        "is_active",
        "employment_status",
        "employment_type",
        "office",
        "department",
        "designation",
    ]
    search_fields = [
        "employee_id",
        "user__first_name",
        "user__last_name",
        "user__email",
    ]
    raw_id_fields = ["user", "office", "department", "designation", "created_by"]
    ordering = ["employee_id"]
    inlines = [EmployeeSystemInline]

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = "Full Name"


@admin.register(EmployeeSystem)
class EmployeeSystemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "employee",
        "computer_name",
        "ip_address",
        "operating_system",
        "is_active",
        "assigned_at",
    ]
    list_filter = ["is_active", "operating_system"]
    search_fields = [
        "employee__employee_id",
        "computer_name",
        "ip_address",
        "domain_username",
    ]
    raw_id_fields = ["employee", "updated_by"]


@admin.register(EmployeeTransfer)
class EmployeeTransferAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "employee",
        "from_office",
        "to_office",
        "transfer_date",
        "status",
        "initiated_by",
        "approved_by",
    ]
    list_filter = ["status", "from_office", "to_office"]
    search_fields = [
        "employee__employee_id",
        "order_number",
        "employee__user__first_name",
        "employee__user__last_name",
    ]
    raw_id_fields = [
        "employee",
        "from_office",
        "to_office",
        "from_department",
        "to_department",
        "from_designation",
        "to_designation",
        "initiated_by",
        "approved_by",
    ]
    ordering = ["-transfer_date"]
    readonly_fields = ["approved_at"]
