from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    Department,
    Designation,
    Office,
    Employee,
    EmployeeSystem,
    EmployeeTransfer,
)

User = get_user_model()


# ---------------------------------------------------------------------------
# Lookup serializers (minimal, for nested read representations)
# ---------------------------------------------------------------------------


class DepartmentMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "code"]


class DesignationMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ["id", "name", "code"]


class OfficeMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ["id", "name", "code", "office_type"]


# ---------------------------------------------------------------------------
# Department
# ---------------------------------------------------------------------------


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        qs = Department.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A department with this name already exists."
            )
        return value


# ---------------------------------------------------------------------------
# Designation
# ---------------------------------------------------------------------------


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = [
            "id",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        qs = Designation.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A designation with this name already exists."
            )
        return value


# ---------------------------------------------------------------------------
# Office
# ---------------------------------------------------------------------------


class OfficeSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(
        source="district.name", read_only=True
    )
    state_name = serializers.CharField(
        source="district.state.name", read_only=True
    )
    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Office
        fields = [
            "id",
            "name",
            "code",
            "office_type",
            "district",
            "district_name",
            "state_name",
            "address",
            "phone",
            "email",
            "is_active",
            "employee_count",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "district_name",
            "state_name",
            "created_by",
            "created_by_name",
            "employee_count",
            "created_at",
            "updated_at",
        ]

    def get_employee_count(self, obj):
        return obj.employees.filter(is_active=True).count()

    def validate_code(self, value):
        qs = Office.objects.filter(code__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "An office with this code already exists."
            )
        return value.upper()


# ---------------------------------------------------------------------------
# Employee
# ---------------------------------------------------------------------------


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer used in list views and nested representations."""

    full_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    office_name = serializers.CharField(source="office.name", read_only=True)
    department_name = serializers.CharField(
        source="department.name", read_only=True
    )
    designation_name = serializers.CharField(
        source="designation.name", read_only=True
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "full_name",
            "email",
            "office_name",
            "department_name",
            "designation_name",
            "employment_type",
            "employment_status",
            "is_active",
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    # Nested read representations
    office_detail = OfficeMinimalSerializer(source="office", read_only=True)
    department_detail = DepartmentMinimalSerializer(
        source="department", read_only=True
    )
    designation_detail = DesignationMinimalSerializer(
        source="designation", read_only=True
    )
    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "user",
            "employee_id",
            "full_name",
            "email",
            "office",
            "office_detail",
            "department",
            "department_detail",
            "designation",
            "designation_detail",
            "gender",
            "date_of_birth",
            "phone",
            "address",
            "date_of_joining",
            "employment_type",
            "employment_status",
            "is_active",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "full_name",
            "email",
            "office_detail",
            "department_detail",
            "designation_detail",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]

    def validate_user(self, value):
        qs = Employee.objects.filter(user=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "An employee profile already exists for this user."
            )
        return value

    def validate_employee_id(self, value):
        qs = Employee.objects.filter(employee_id__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "An employee with this ID already exists."
            )
        return value.upper()


# ---------------------------------------------------------------------------
# EmployeeSystem
# ---------------------------------------------------------------------------


class EmployeeSystemSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(
        source="employee.employee_id", read_only=True
    )
    employee_name = serializers.CharField(
        source="employee.full_name", read_only=True
    )
    updated_by_name = serializers.CharField(
        source="updated_by.get_full_name", read_only=True
    )

    class Meta:
        model = EmployeeSystem
        fields = [
            "id",
            "employee",
            "employee_id",
            "employee_name",
            "computer_name",
            "ip_address",
            "mac_address",
            "operating_system",
            "os_version",
            "domain_username",
            "system_notes",
            "assigned_at",
            "is_active",
            "updated_by",
            "updated_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee_id",
            "employee_name",
            "updated_by",
            "updated_by_name",
            "created_at",
            "updated_at",
        ]

    def validate_employee(self, value):
        qs = EmployeeSystem.objects.filter(employee=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "System details already exist for this employee."
            )
        return value


# ---------------------------------------------------------------------------
# EmployeeTransfer
# ---------------------------------------------------------------------------


class EmployeeTransferSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source="employee.full_name", read_only=True
    )
    employee_code = serializers.CharField(
        source="employee.employee_id", read_only=True
    )
    from_office_name = serializers.CharField(
        source="from_office.name", read_only=True
    )
    to_office_name = serializers.CharField(
        source="to_office.name", read_only=True
    )
    from_department_name = serializers.CharField(
        source="from_department.name", read_only=True
    )
    to_department_name = serializers.CharField(
        source="to_department.name", read_only=True
    )
    from_designation_name = serializers.CharField(
        source="from_designation.name", read_only=True
    )
    to_designation_name = serializers.CharField(
        source="to_designation.name", read_only=True
    )
    initiated_by_name = serializers.CharField(
        source="initiated_by.get_full_name", read_only=True
    )
    approved_by_name = serializers.CharField(
        source="approved_by.get_full_name", read_only=True
    )

    class Meta:
        model = EmployeeTransfer
        fields = [
            "id",
            "employee",
            "employee_name",
            "employee_code",
            "from_office",
            "from_office_name",
            "to_office",
            "to_office_name",
            "from_department",
            "from_department_name",
            "to_department",
            "to_department_name",
            "from_designation",
            "from_designation_name",
            "to_designation",
            "to_designation_name",
            "transfer_date",
            "effective_date",
            "order_number",
            "reason",
            "remarks",
            "status",
            "initiated_by",
            "initiated_by_name",
            "approved_by",
            "approved_by_name",
            "approved_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee_name",
            "employee_code",
            "from_office_name",
            "to_office_name",
            "from_department_name",
            "to_department_name",
            "from_designation_name",
            "to_designation_name",
            "initiated_by",
            "initiated_by_name",
            "approved_by",
            "approved_by_name",
            "approved_at",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        if data.get("from_office") and data.get("to_office"):
            if data["from_office"] == data["to_office"]:
                raise serializers.ValidationError(
                    {"to_office": "Source and destination office must be different."}
                )
        return data


class EmployeeTransferStatusSerializer(serializers.Serializer):
    """Used exclusively for approve / reject / complete actions."""

    status = serializers.ChoiceField(
        choices=["APPROVED", "REJECTED", "COMPLETED", "CANCELLED"]
    )
    remarks = serializers.CharField(required=False, allow_blank=True)
