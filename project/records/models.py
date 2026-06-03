from django.db import models
from django.conf import settings


class Department(models.Model):
    """Department within an office (e.g. Finance, HR, Engineering)."""

    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employees_department"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Designation(models.Model):
    """Job title / designation (e.g. Senior Engineer, Manager)."""

    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employees_designation"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Office(models.Model):
    """Physical / administrative office tied to a District."""

    OFFICE_TYPE_CHOICES = [
        ("HEAD", "Head Office"),
        ("REGIONAL", "Regional Office"),
        ("DISTRICT", "District Office"),
        ("SUB", "Sub Office"),
        ("OTHER", "Other"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    office_type = models.CharField(
        max_length=20, choices=OFFICE_TYPE_CHOICES, default="OTHER"
    )
    district = models.ForeignKey(
        "users.District",  # existing District model from users app
        on_delete=models.PROTECT,
        related_name="offices",
    )
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offices_created",
    )

    class Meta:
        db_table = "employees_office"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Employee(models.Model):
    """Employee record linked 1-to-1 with an existing User account."""

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    EMPLOYMENT_STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("SUSPENDED", "Suspended"),
        ("TERMINATED", "Terminated"),
        ("RETIRED", "Retired"),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ("PERMANENT", "Permanent"),
        ("CONTRACT", "Contract"),
        ("PROBATION", "Probation"),
        ("DEPUTATION", "Deputation"),
        ("TEMPORARY", "Temporary"),
    ]

    # Core link to existing User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="employee_profile",
    )

    # Organisational placement
    office = models.ForeignKey(
        Office,
        on_delete=models.PROTECT,
        related_name="employees",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    # Identity
    employee_id = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Service details
    date_of_joining = models.DateField()
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default="PERMANENT",
    )
    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default="ACTIVE",
    )

    # Audit
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees_created",
    )

    class Meta:
        db_table = "employees_employee"
        ordering = ["employee_id"]

    def __str__(self):
        return f"{self.employee_id} – {self.user.get_full_name()}"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email


class EmployeeSystem(models.Model):
    """System / IT access details attached to an Employee."""

    OS_CHOICES = [
        ("WINDOWS", "Windows"),
        ("LINUX", "Linux"),
        ("MACOS", "macOS"),
        ("OTHER", "Other"),
    ]

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="system_details",
    )

    computer_name = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    operating_system = models.CharField(
        max_length=20, choices=OS_CHOICES, blank=True, null=True
    )
    os_version = models.CharField(max_length=100, blank=True, null=True)

    # Access credentials / notes (no raw passwords stored here)
    domain_username = models.CharField(max_length=255, blank=True, null=True)
    system_notes = models.TextField(blank=True, null=True)

    assigned_at = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="system_records_updated",
    )

    class Meta:
        db_table = "employees_employee_system"
        verbose_name = "Employee System Detail"
        verbose_name_plural = "Employee System Details"

    def __str__(self):
        return f"System – {self.employee.employee_id}"


class EmployeeTransfer(models.Model):
    """Records an inter-office transfer for an Employee."""

    TRANSFER_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="transfers",
    )

    from_office = models.ForeignKey(
        Office,
        on_delete=models.PROTECT,
        related_name="transfers_out",
    )
    to_office = models.ForeignKey(
        Office,
        on_delete=models.PROTECT,
        related_name="transfers_in",
    )
    from_department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="transfers_out",
        null=True,
        blank=True,
    )
    to_department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="transfers_in",
        null=True,
        blank=True,
    )
    from_designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT,
        related_name="transfers_out",
        null=True,
        blank=True,
    )
    to_designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT,
        related_name="transfers_in",
        null=True,
        blank=True,
    )

    transfer_date = models.DateField()
    effective_date = models.DateField(blank=True, null=True)
    order_number = models.CharField(max_length=100, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=TRANSFER_STATUS_CHOICES,
        default="PENDING",
    )

    # Approval chain
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transfers_initiated",
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transfers_approved",
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employees_employee_transfer"
        ordering = ["-transfer_date"]

    def __str__(self):
        return (
            f"Transfer #{self.pk} – {self.employee.employee_id} "
            f"({self.from_office} → {self.to_office})"
        )
