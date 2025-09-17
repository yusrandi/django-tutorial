from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializer import EmployeeSerializer
from .models import Employee


# Create your views here.
class EmployeeView(ViewSet):
    # GET /api/employees
    def list(self, request):
        # ORM ini bhasa lainnya dari SQL "Select *from employee"
        employees = Employee.objects.all()

        # serializer ini adalah convert dari model ke json
        serializer = EmployeeSerializer(employees, many=True)

        return Response({"data": serializer.data})

    # POST
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Berhasil"})
        else:
            return Response({"status": "Gagal"})

    # PUT
    def update(self, request, pk=None):
        employee = Employee.objects.get(pk=pk)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Berhasil Update"})
        else:
            return Response({"status": "Gagal Update"})

    # DELETE
    def delete(self, request, pk=None):
        employee = Employee.objects.get(pk=pk)
        employee.delete()
        return Response({"status": "Berhasil Delete"})
