from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import (
    Department,
    Designation,
    Office,
    Employee,
    EmployeeSystem,
    EmployeeTransfer,
)
from .serializers import (
    DepartmentSerializer,
    DesignationSerializer,
    OfficeSerializer,
    EmployeeSerializer,
    EmployeeListSerializer,
    EmployeeSystemSerializer,
    EmployeeTransferSerializer,
    EmployeeTransferStatusSerializer,
)
from .permissions import (
    CanManageDepartment,
    CanManageDesignation,
    CanManageOffice,
    CanViewOffice,
    CanManageEmployee,
    CanViewEmployee,
    CanManageEmployeeSystem,
    CanViewEmployeeSystem,
    CanInitiateTransfer,
    CanApproveTransfer,
    CanViewTransfer,
    CanViewDashboard,
)
from .services import (
    DepartmentService,
    DesignationService,
    OfficeService,
    EmployeeService,
    EmployeeSystemService,
    EmployeeTransferService,
    DashboardService,
)


# ===========================================================================
# Department views
# ===========================================================================


class DepartmentListCreateView(APIView):
    """GET /departments/  |  POST /departments/"""

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CanManageDepartment()]
        return [IsAuthenticated()]

    def get(self, request):
        filters = {
            "search": request.query_params.get("search"),
            "is_active": request.query_params.get("is_active"),
        }
        # Convert string booleans from query params
        if filters["is_active"] is not None:
            filters["is_active"] = filters["is_active"].lower() == "true"
        else:
            filters.pop("is_active")

        queryset = DepartmentService.get_list(filters)
        serializer = DepartmentSerializer(queryset, many=True)
        return Response({"message": "Departments fetched successfully.", "data": serializer.data})

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        department = DepartmentService.create(serializer.validated_data)
        return Response(
            {"message": "Department created successfully.", "data": DepartmentSerializer(department).data},
            status=status.HTTP_201_CREATED,
        )


class DepartmentDetailView(APIView):
    """GET /departments/<pk>/  |  PUT /departments/<pk>/  |  DELETE /departments/<pk>/"""

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAuthenticated(), CanManageDepartment()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        return get_object_or_404(Department, pk=pk)

    def get(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department)
        return Response({"message": "Department fetched successfully.", "data": serializer.data})

    def put(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        department = DepartmentService.update(department, serializer.validated_data)
        return Response({"message": "Department updated successfully.", "data": DepartmentSerializer(department).data})

    def patch(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        department = DepartmentService.update(department, serializer.validated_data)
        return Response({"message": "Department updated successfully.", "data": DepartmentSerializer(department).data})

    def delete(self, request, pk):
        department = self.get_object(pk)
        try:
            DepartmentService.delete(department)
        except ValueError as exc:
            return Response({"message": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Department deactivated successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# Designation views
# ===========================================================================


class DesignationListCreateView(APIView):
    """GET /designations/  |  POST /designations/"""

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CanManageDesignation()]
        return [IsAuthenticated()]

    def get(self, request):
        filters = {
            "search": request.query_params.get("search"),
        }
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            filters["is_active"] = is_active.lower() == "true"

        queryset = DesignationService.get_list(filters)
        serializer = DesignationSerializer(queryset, many=True)
        return Response({"message": "Designations fetched successfully.", "data": serializer.data})

    def post(self, request):
        serializer = DesignationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        designation = DesignationService.create(serializer.validated_data)
        return Response(
            {"message": "Designation created successfully.", "data": DesignationSerializer(designation).data},
            status=status.HTTP_201_CREATED,
        )


class DesignationDetailView(APIView):
    """GET /designations/<pk>/  |  PUT/PATCH /designations/<pk>/  |  DELETE /designations/<pk>/"""

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAuthenticated(), CanManageDesignation()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        return get_object_or_404(Designation, pk=pk)

    def get(self, request, pk):
        designation = self.get_object(pk)
        serializer = DesignationSerializer(designation)
        return Response({"message": "Designation fetched successfully.", "data": serializer.data})

    def put(self, request, pk):
        designation = self.get_object(pk)
        serializer = DesignationSerializer(designation, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        designation = DesignationService.update(designation, serializer.validated_data)
        return Response({"message": "Designation updated successfully.", "data": DesignationSerializer(designation).data})

    def patch(self, request, pk):
        designation = self.get_object(pk)
        serializer = DesignationSerializer(designation, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        designation = DesignationService.update(designation, serializer.validated_data)
        return Response({"message": "Designation updated successfully.", "data": DesignationSerializer(designation).data})

    def delete(self, request, pk):
        designation = self.get_object(pk)
        try:
            DesignationService.delete(designation)
        except ValueError as exc:
            return Response({"message": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Designation deactivated successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# Office views
# ===========================================================================


class OfficeListCreateView(APIView):
    """GET /offices/  |  POST /offices/"""

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CanManageOffice()]
        return [IsAuthenticated(), CanViewOffice()]

    def get(self, request):
        filters = {
            "search": request.query_params.get("search"),
            "district_id": request.query_params.get("district_id"),
            "office_type": request.query_params.get("office_type"),
        }
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            filters["is_active"] = is_active.lower() == "true"

        queryset = OfficeService.get_list(filters)
        serializer = OfficeSerializer(queryset, many=True)
        return Response({"message": "Offices fetched successfully.", "data": serializer.data})

    def post(self, request):
        serializer = OfficeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        office = OfficeService.create(serializer.validated_data, created_by=request.user)
        return Response(
            {"message": "Office created successfully.", "data": OfficeSerializer(office).data},
            status=status.HTTP_201_CREATED,
        )


class OfficeDetailView(APIView):
    """GET /offices/<pk>/  |  PUT/PATCH /offices/<pk>/  |  DELETE /offices/<pk>/"""

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAuthenticated(), CanManageOffice()]
        return [IsAuthenticated(), CanViewOffice()]

    def get_object(self, pk):
        return get_object_or_404(Office, pk=pk)

    def get(self, request, pk):
        office = self.get_object(pk)
        serializer = OfficeSerializer(office)
        return Response({"message": "Office fetched successfully.", "data": serializer.data})

    def put(self, request, pk):
        office = self.get_object(pk)
        serializer = OfficeSerializer(office, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        office = OfficeService.update(office, serializer.validated_data)
        return Response({"message": "Office updated successfully.", "data": OfficeSerializer(office).data})

    def patch(self, request, pk):
        office = self.get_object(pk)
        serializer = OfficeSerializer(office, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        office = OfficeService.update(office, serializer.validated_data)
        return Response({"message": "Office updated successfully.", "data": OfficeSerializer(office).data})

    def delete(self, request, pk):
        office = self.get_object(pk)
        try:
            OfficeService.delete(office)
        except ValueError as exc:
            return Response({"message": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Office deactivated successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# Employee views
# ===========================================================================


class EmployeeListCreateView(APIView):
    """GET /employees/  |  POST /employees/"""

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CanManageEmployee()]
        return [IsAuthenticated(), CanViewEmployee()]

    def get(self, request):
        filters = {
            "search": request.query_params.get("search"),
            "office_id": request.query_params.get("office_id"),
            "department_id": request.query_params.get("department_id"),
            "designation_id": request.query_params.get("designation_id"),
            "employment_status": request.query_params.get("employment_status"),
            "employment_type": request.query_params.get("employment_type"),
        }
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            filters["is_active"] = is_active.lower() == "true"

        queryset = EmployeeService.get_list(filters)
        serializer = EmployeeListSerializer(queryset, many=True)
        return Response(
            {
                "message": "Employees fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data,
            }
        )

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        employee = EmployeeService.create(
            serializer.validated_data, created_by=request.user
        )
        return Response(
            {"message": "Employee created successfully.", "data": EmployeeSerializer(employee).data},
            status=status.HTTP_201_CREATED,
        )


class EmployeeDetailView(APIView):
    """GET /employees/<pk>/  |  PUT/PATCH /employees/<pk>/  |  DELETE /employees/<pk>/"""

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAuthenticated(), CanManageEmployee()]
        return [IsAuthenticated(), CanViewEmployee()]

    def get_object(self, pk):
        return get_object_or_404(
            Employee.objects.select_related(
                "user", "office", "department", "designation"
            ),
            pk=pk,
        )

    def get(self, request, pk):
        employee = self.get_object(pk)
        # Object-level permission check
        perm = CanViewEmployee()
        if not perm.has_object_permission(request, self, employee):
            return Response(
                {"message": "You do not have permission to view this employee."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = EmployeeSerializer(employee)
        return Response({"message": "Employee fetched successfully.", "data": serializer.data})

    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        employee = EmployeeService.update(employee, serializer.validated_data)
        return Response({"message": "Employee updated successfully.", "data": EmployeeSerializer(employee).data})

    def patch(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        employee = EmployeeService.update(employee, serializer.validated_data)
        return Response({"message": "Employee updated successfully.", "data": EmployeeSerializer(employee).data})

    def delete(self, request, pk):
        employee = self.get_object(pk)
        EmployeeService.deactivate(employee)
        return Response({"message": "Employee deactivated successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# EmployeeSystem views
# ===========================================================================


class EmployeeSystemListCreateView(APIView):
    """GET /employee-systems/  |  POST /employee-systems/"""

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CanManageEmployeeSystem()]
        return [IsAuthenticated(), CanViewEmployeeSystem()]

    def get(self, request):
        filters = {
            "employee_id": request.query_params.get("employee_id"),
        }
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            filters["is_active"] = is_active.lower() == "true"

        queryset = EmployeeSystemService.get_list(filters)
        serializer = EmployeeSystemSerializer(queryset, many=True)
        return Response({"message": "Employee system records fetched.", "data": serializer.data})

    def post(self, request):
        serializer = EmployeeSystemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        record = EmployeeSystemService.create(
            serializer.validated_data, updated_by=request.user
        )
        return Response(
            {"message": "Employee system details added.", "data": EmployeeSystemSerializer(record).data},
            status=status.HTTP_201_CREATED,
        )


class EmployeeSystemDetailView(APIView):
    """GET /employee-systems/<pk>/  |  PUT/PATCH /employee-systems/<pk>/"""

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH"):
            return [IsAuthenticated(), CanManageEmployeeSystem()]
        return [IsAuthenticated(), CanViewEmployeeSystem()]

    def get_object(self, pk):
        return get_object_or_404(
            EmployeeSystem.objects.select_related("employee", "employee__user"),
            pk=pk,
        )

    def get(self, request, pk):
        record = self.get_object(pk)
        perm = CanViewEmployeeSystem()
        if not perm.has_object_permission(request, self, record):
            return Response(
                {"message": "You do not have permission to view this record."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = EmployeeSystemSerializer(record)
        return Response({"message": "Employee system details fetched.", "data": serializer.data})

    def put(self, request, pk):
        record = self.get_object(pk)
        serializer = EmployeeSystemSerializer(record, data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        record = EmployeeSystemService.update(
            record, serializer.validated_data, updated_by=request.user
        )
        return Response({"message": "Employee system details updated.", "data": EmployeeSystemSerializer(record).data})

    def patch(self, request, pk):
        record = self.get_object(pk)
        serializer = EmployeeSystemSerializer(record, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        record = EmployeeSystemService.update(
            record, serializer.validated_data, updated_by=request.user
        )
        return Response({"message": "Employee system details updated.", "data": EmployeeSystemSerializer(record).data})


class EmployeeSystemByEmployeeView(APIView):
    """GET /employees/<employee_pk>/system/ – convenience endpoint."""

    permission_classes = [IsAuthenticated, CanViewEmployeeSystem]

    def get(self, request, employee_pk):
        employee = get_object_or_404(Employee, pk=employee_pk)
        record = get_object_or_404(EmployeeSystem, employee=employee)

        perm = CanViewEmployeeSystem()
        if not perm.has_object_permission(request, self, record):
            return Response(
                {"message": "You do not have permission to view this record."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = EmployeeSystemSerializer(record)
        return Response({"message": "Employee system details fetched.", "data": serializer.data})


# ===========================================================================
# EmployeeTransfer views
# ===========================================================================


class EmployeeTransferListCreateView(APIView):
    """GET /employee-transfers/  |  POST /employee-transfers/"""

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CanInitiateTransfer()]
        return [IsAuthenticated(), CanViewTransfer()]

    def get(self, request):
        filters = {
            "employee_id": request.query_params.get("employee_id"),
            "status": request.query_params.get("status"),
            "from_office_id": request.query_params.get("from_office_id"),
            "to_office_id": request.query_params.get("to_office_id"),
        }
        queryset = EmployeeTransferService.get_list(filters)
        serializer = EmployeeTransferSerializer(queryset, many=True)
        return Response(
            {
                "message": "Employee transfers fetched successfully.",
                "count": queryset.count(),
                "data": serializer.data,
            }
        )

    def post(self, request):
        serializer = EmployeeTransferSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        transfer = EmployeeTransferService.initiate(
            serializer.validated_data, initiated_by=request.user
        )
        return Response(
            {"message": "Transfer initiated successfully.", "data": EmployeeTransferSerializer(transfer).data},
            status=status.HTTP_201_CREATED,
        )


class EmployeeTransferDetailView(APIView):
    """GET /employee-transfers/<pk>/"""

    permission_classes = [IsAuthenticated, CanViewTransfer]

    def get_object(self, pk):
        return get_object_or_404(EmployeeTransfer, pk=pk)

    def get(self, request, pk):
        transfer = self.get_object(pk)
        perm = CanViewTransfer()
        if not perm.has_object_permission(request, self, transfer):
            return Response(
                {"message": "You do not have permission to view this transfer."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = EmployeeTransferSerializer(transfer)
        return Response({"message": "Transfer fetched successfully.", "data": serializer.data})


class EmployeeTransferStatusUpdateView(APIView):
    """
    PATCH /employee-transfers/<pk>/status/
    Approve, reject, complete, or cancel a transfer.
    """

    permission_classes = [IsAuthenticated, CanApproveTransfer]

    def get_object(self, pk):
        return get_object_or_404(EmployeeTransfer, pk=pk)

    def patch(self, request, pk):
        transfer = self.get_object(pk)
        serializer = EmployeeTransferStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Validation failed.", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            transfer = EmployeeTransferService.update_status(
                transfer,
                status=serializer.validated_data["status"],
                approved_by=request.user,
                remarks=serializer.validated_data.get("remarks", ""),
            )
        except ValueError as exc:
            return Response({"message": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "message": f"Transfer status updated to '{transfer.status}'.",
                "data": EmployeeTransferSerializer(transfer).data,
            }
        )


class EmployeeTransfersByEmployeeView(APIView):
    """GET /employees/<employee_pk>/transfers/ – all transfers for a specific employee."""

    permission_classes = [IsAuthenticated, CanViewTransfer]

    def get(self, request, employee_pk):
        employee = get_object_or_404(Employee, pk=employee_pk)
        perm = CanViewTransfer()
        # Reuse object permission: treat employee object as the transfer's employee
        if request.user.get_role_name() not in ["Admin", "HR", "Manager"]:
            if not (hasattr(employee, "user") and employee.user == request.user):
                return Response(
                    {"message": "You do not have permission to view these transfers."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        transfers = EmployeeTransfer.objects.filter(employee=employee).order_by(
            "-transfer_date"
        )
        serializer = EmployeeTransferSerializer(transfers, many=True)
        return Response(
            {
                "message": "Employee transfers fetched.",
                "count": transfers.count(),
                "data": serializer.data,
            }
        )


# ===========================================================================
# Dashboard view
# ===========================================================================


class DashboardView(APIView):
    """GET /dashboard/ – summary statistics."""

    permission_classes = [IsAuthenticated, CanViewDashboard]

    def get(self, request):
        data = DashboardService.get_summary(request.user)
        return Response({"message": "Dashboard data fetched successfully.", "data": data})
