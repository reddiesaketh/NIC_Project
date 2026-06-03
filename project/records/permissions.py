from rest_framework.permissions import BasePermission, IsAuthenticated


# ---------------------------------------------------------------------------
# Role constants – mirror whatever role names exist in the users app
# ---------------------------------------------------------------------------

ROLE_ADMIN = "Admin"
ROLE_HR = "HR"
ROLE_MANAGER = "Manager"
ROLE_EMPLOYEE = "Employee"
ROLE_VIEWER = "Viewer"

ADMIN_ROLES = [ROLE_ADMIN]
HR_ROLES = [ROLE_ADMIN, ROLE_HR]
MANAGEMENT_ROLES = [ROLE_ADMIN, ROLE_HR, ROLE_MANAGER]
ALL_STAFF_ROLES = [ROLE_ADMIN, ROLE_HR, ROLE_MANAGER, ROLE_EMPLOYEE]


def _get_role(request):
    """Return the role name string for the authenticated user."""
    try:
        return request.user.get_role_name()
    except AttributeError:
        return None


# ---------------------------------------------------------------------------
# Office permissions
# ---------------------------------------------------------------------------


class CanManageOffice(BasePermission):
    """Create / update / delete offices – Admin or HR only."""

    message = "You do not have permission to manage offices."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and _get_role(request) in HR_ROLES
        )


class CanViewOffice(BasePermission):
    """Any authenticated staff member can view offices."""

    message = "You must be authenticated to view offices."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


# ---------------------------------------------------------------------------
# Department / Designation permissions
# ---------------------------------------------------------------------------


class CanManageDepartment(BasePermission):
    """Create / update / delete departments – Admin or HR only."""

    message = "You do not have permission to manage departments."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and _get_role(request) in HR_ROLES
        )


class CanManageDesignation(BasePermission):
    """Create / update / delete designations – Admin or HR only."""

    message = "You do not have permission to manage designations."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and _get_role(request) in HR_ROLES
        )


# ---------------------------------------------------------------------------
# Employee permissions
# ---------------------------------------------------------------------------


class CanManageEmployee(BasePermission):
    """Create / update / delete employee records – Admin or HR."""

    message = "You do not have permission to manage employee records."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and _get_role(request) in HR_ROLES
        )


class CanViewEmployee(BasePermission):
    """
    Any authenticated user can view employee list / detail.
    Employees can additionally only be allowed to see their own profile
    (enforced at the view level using has_object_permission).
    """

    message = "You must be authenticated to view employee records."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        role = _get_role(request)
        if role in MANAGEMENT_ROLES:
            return True
        # Regular employees can only see their own profile
        return hasattr(obj, "user") and obj.user == request.user


# ---------------------------------------------------------------------------
# Employee System Details permissions
# ---------------------------------------------------------------------------


class CanManageEmployeeSystem(BasePermission):
    """Manage system details – Admin or HR."""

    message = "You do not have permission to manage employee system details."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and _get_role(request) in HR_ROLES
        )


class CanViewEmployeeSystem(BasePermission):
    """
    Admin/HR/Manager can view all; employee can view their own.
    Object-level check enforced in views.
    """

    message = "You must be authenticated to view system details."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        role = _get_role(request)
        if role in MANAGEMENT_ROLES:
            return True
        return (
            hasattr(obj, "employee")
            and hasattr(obj.employee, "user")
            and obj.employee.user == request.user
        )


# ---------------------------------------------------------------------------
# Employee Transfer permissions
# ---------------------------------------------------------------------------


class CanInitiateTransfer(BasePermission):
    """HR and Managers can initiate transfers; Admins always can."""

    message = "You do not have permission to initiate employee transfers."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and _get_role(request) in MANAGEMENT_ROLES
        )


class CanApproveTransfer(BasePermission):
    """Only Admin or HR can approve/reject transfers."""

    message = "You do not have permission to approve or reject transfers."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and _get_role(request) in HR_ROLES
        )


class CanViewTransfer(BasePermission):
    """Any authenticated user; object-level check restricts employees to own."""

    message = "You must be authenticated to view transfers."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        role = _get_role(request)
        if role in MANAGEMENT_ROLES:
            return True
        return (
            hasattr(obj, "employee")
            and hasattr(obj.employee, "user")
            and obj.employee.user == request.user
        )


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------


class CanViewDashboard(BasePermission):
    """Any authenticated user can view the dashboard."""

    message = "You must be authenticated to view the dashboard."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
