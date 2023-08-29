from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from . import models
from . import serializers
from .permissions import FullDjangoModelPermissions


class DepartmentViewset(ModelViewSet):
    permission_classes = [FullDjangoModelPermissions]
    serializer_class = serializers.DepartmentSerializer
    queryset = models.Department.objects.all()

    def destroy(self, request, *args, **kwargs):
        if models.Employee.objects.filter(department_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Department cannot be deleted because it cantains employee(s).'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif models.Teacher.objects.filter(department_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Department cannot be deleted because it contains teacher(s)'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif models.Student.objects.filter(department_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Department cannot be deleted because it contains student(s)'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
