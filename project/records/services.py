"""
Business-logic layer for the employees app.
All database mutations go through these service functions so that views stay
thin and logic is easily testable in isolation.
"""

from django.db import transaction
from django.utils import timezone

from .models import (
    Department,
    Designation,
    Office,
    Employee,
    EmployeeSystem,
    EmployeeTransfer,
)


# ---------------------------------------------------------------------------
# Department services
# ---------------------------------------------------------------------------


class DepartmentService:

    @staticmethod
    @transaction.atomic
    def create(validated_data: dict) -> Department:
        return Department.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(instance: Department, validated_data: dict) -> Department:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance: Department) -> None:
        if instance.employees.filter(is_active=True).exists():
            raise ValueError(
                "Cannot delete a department that has active employees."
            )
        instance.is_active = False
        instance.save(update_fields=["is_active"])

    @staticmethod
    def get_list(filters: dict = None):
        qs = Department.objects.all()
        if filters:
            if "is_active" in filters:
                qs = qs.filter(is_active=filters["is_active"])
            if filters.get("search"):
                qs = qs.filter(name__icontains=filters["search"])
        return qs.order_by("name")


# ---------------------------------------------------------------------------
# Designation services
# ---------------------------------------------------------------------------


class DesignationService:

    @staticmethod
    @transaction.atomic
    def create(validated_data: dict) -> Designation:
        return Designation.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(instance: Designation, validated_data: dict) -> Designation:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance: Designation) -> None:
        if instance.employees.filter(is_active=True).exists():
            raise ValueError(
                "Cannot delete a designation that has active employees."
            )
        instance.is_active = False
        instance.save(update_fields=["is_active"])

    @staticmethod
    def get_list(filters: dict = None):
        qs = Designation.objects.all()
        if filters:
            if "is_active" in filters:
                qs = qs.filter(is_active=filters["is_active"])
            if filters.get("search"):
                qs = qs.filter(name__icontains=filters["search"])
        return qs.order_by("name")


# ---------------------------------------------------------------------------
# Office services
# ---------------------------------------------------------------------------


class OfficeService:

    @staticmethod
    @transaction.atomic
    def create(validated_data: dict, created_by) -> Office:
        validated_data["created_by"] = created_by
        return Office.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(instance: Office, validated_data: dict) -> Office:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance: Office) -> None:
        if instance.employees.filter(is_active=True).exists():
            raise ValueError(
                "Cannot delete an office that has active employees assigned."
            )
        instance.is_active = False
        instance.save(update_fields=["is_active"])

    @staticmethod
    def get_list(filters: dict = None):
        qs = Office.objects.select_related("district", "district__state").all()
        if filters:
            if "is_active" in filters:
                qs = qs.filter(is_active=filters["is_active"])
            if filters.get("district_id"):
                qs = qs.filter(district_id=filters["district_id"])
            if filters.get("office_type"):
                qs = qs.filter(office_type=filters["office_type"])
            if filters.get("search"):
                qs = qs.filter(name__icontains=filters["search"])
        return qs.order_by("name")


# ---------------------------------------------------------------------------
# Employee services
# ---------------------------------------------------------------------------


class EmployeeService:

    @staticmethod
    @transaction.atomic
    def create(validated_data: dict, created_by) -> Employee:
        validated_data["created_by"] = created_by
        return Employee.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(instance: Employee, validated_data: dict) -> Employee:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def deactivate(instance: Employee) -> None:
        instance.is_active = False
        instance.employment_status = "INACTIVE"
        instance.save(update_fields=["is_active", "employment_status"])

    @staticmethod
    def get_list(filters: dict = None):
        qs = Employee.objects.select_related(
            "user",
            "office",
            "department",
            "designation",
        ).all()
        if filters:
            if "is_active" in filters:
                qs = qs.filter(is_active=filters["is_active"])
            if filters.get("office_id"):
                qs = qs.filter(office_id=filters["office_id"])
            if filters.get("department_id"):
                qs = qs.filter(department_id=filters["department_id"])
            if filters.get("designation_id"):
                qs = qs.filter(designation_id=filters["designation_id"])
            if filters.get("employment_status"):
                qs = qs.filter(employment_status=filters["employment_status"])
            if filters.get("employment_type"):
                qs = qs.filter(employment_type=filters["employment_type"])
            if filters.get("search"):
                term = filters["search"]
                qs = qs.filter(
                    employee_id__icontains=term
                ) | qs.filter(
                    user__first_name__icontains=term
                ) | qs.filter(
                    user__last_name__icontains=term
                ) | qs.filter(
                    user__email__icontains=term
                )
        return qs.order_by("employee_id")


# ---------------------------------------------------------------------------
# EmployeeSystem services
# ---------------------------------------------------------------------------


class EmployeeSystemService:

    @staticmethod
    @transaction.atomic
    def create(validated_data: dict, updated_by) -> EmployeeSystem:
        validated_data["updated_by"] = updated_by
        return EmployeeSystem.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update(
        instance: EmployeeSystem, validated_data: dict, updated_by
    ) -> EmployeeSystem:
        validated_data["updated_by"] = updated_by
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    def get_list(filters: dict = None):
        qs = EmployeeSystem.objects.select_related(
            "employee", "employee__user"
        ).all()
        if filters:
            if "is_active" in filters:
                qs = qs.filter(is_active=filters["is_active"])
            if filters.get("employee_id"):
                qs = qs.filter(employee_id=filters["employee_id"])
        return qs.order_by("employee__employee_id")


# ---------------------------------------------------------------------------
# EmployeeTransfer services
# ---------------------------------------------------------------------------


class EmployeeTransferService:

    @staticmethod
    @transaction.atomic
    def initiate(validated_data: dict, initiated_by) -> EmployeeTransfer:
        employee: Employee = validated_data["employee"]

        # Auto-populate source office / department / designation from current profile
        validated_data.setdefault("from_office", employee.office)
        validated_data.setdefault("from_department", employee.department)
        validated_data.setdefault("from_designation", employee.designation)
        validated_data["initiated_by"] = initiated_by
        validated_data["status"] = "PENDING"

        return EmployeeTransfer.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update_status(
        instance: EmployeeTransfer,
        status: str,
        approved_by,
        remarks: str = "",
    ) -> EmployeeTransfer:
        allowed_transitions = {
            "PENDING": ["APPROVED", "REJECTED", "CANCELLED"],
            "APPROVED": ["COMPLETED", "CANCELLED"],
            "REJECTED": [],
            "COMPLETED": [],
            "CANCELLED": [],
        }

        if status not in allowed_transitions.get(instance.status, []):
            raise ValueError(
                f"Cannot transition from '{instance.status}' to '{status}'."
            )

        instance.status = status
        instance.remarks = remarks or instance.remarks

        if status in ("APPROVED", "REJECTED"):
            instance.approved_by = approved_by
            instance.approved_at = timezone.now()

        if status == "COMPLETED":
            # Apply transfer: update the employee's profile
            employee = instance.employee
            employee.office = instance.to_office
            if instance.to_department:
                employee.department = instance.to_department
            if instance.to_designation:
                employee.designation = instance.to_designation
            employee.save(update_fields=["office", "department", "designation"])

        instance.save()
        return instance

    @staticmethod
    def get_list(filters: dict = None):
        qs = EmployeeTransfer.objects.select_related(
            "employee",
            "employee__user",
            "from_office",
            "to_office",
            "from_department",
            "to_department",
            "from_designation",
            "to_designation",
            "initiated_by",
            "approved_by",
        ).all()
        if filters:
            if filters.get("employee_id"):
                qs = qs.filter(employee_id=filters["employee_id"])
            if filters.get("status"):
                qs = qs.filter(status=filters["status"])
            if filters.get("from_office_id"):
                qs = qs.filter(from_office_id=filters["from_office_id"])
            if filters.get("to_office_id"):
                qs = qs.filter(to_office_id=filters["to_office_id"])
        return qs.order_by("-transfer_date")


# ---------------------------------------------------------------------------
# Dashboard service
# ---------------------------------------------------------------------------


class DashboardService:

    @staticmethod
    def get_summary(user) -> dict:
        """Return aggregated counts for the dashboard."""

        role = None
        try:
            role = user.get_role_name()
        except AttributeError:
            pass

        total_employees = Employee.objects.filter(is_active=True).count()
        total_offices = Office.objects.filter(is_active=True).count()
        total_departments = Department.objects.filter(is_active=True).count()
        total_designations = Designation.objects.filter(is_active=True).count()

        # Transfer stats
        pending_transfers = EmployeeTransfer.objects.filter(
            status="PENDING"
        ).count()
        completed_transfers = EmployeeTransfer.objects.filter(
            status="COMPLETED"
        ).count()

        # Employment type breakdown
        employment_type_breakdown = {}
        for choice_key, _ in Employee.EMPLOYMENT_TYPE_CHOICES:
            employment_type_breakdown[choice_key] = Employee.objects.filter(
                is_active=True, employment_type=choice_key
            ).count()

        # Employment status breakdown
        employment_status_breakdown = {}
        for choice_key, _ in Employee.EMPLOYMENT_STATUS_CHOICES:
            employment_status_breakdown[choice_key] = Employee.objects.filter(
                employment_status=choice_key
            ).count()

        data = {
            "total_employees": total_employees,
            "total_offices": total_offices,
            "total_departments": total_departments,
            "total_designations": total_designations,
            "pending_transfers": pending_transfers,
            "completed_transfers": completed_transfers,
            "employment_type_breakdown": employment_type_breakdown,
            "employment_status_breakdown": employment_status_breakdown,
        }

        # If the requesting user is an employee, also surface their own info
        if role not in ["Admin", "HR", "Manager"]:
            try:
                emp = Employee.objects.get(user=user)
                data["my_profile"] = {
                    "employee_id": emp.employee_id,
                    "office": emp.office.name,
                    "department": emp.department.name,
                    "designation": emp.designation.name,
                    "employment_status": emp.employment_status,
                }
                data["my_pending_transfers"] = EmployeeTransfer.objects.filter(
                    employee=emp, status="PENDING"
                ).count()
            except Employee.DoesNotExist:
                pass

        return data
