from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from . import models
from . import serializers
from .permissions import FullDjangoModelPermissions
from . import filters


class DepartmentViewset(ModelViewSet):
    permission_classes = [FullDjangoModelPermissions]
    serializer_class = serializers.DepartmentSerializer
    queryset = models.Department.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = filters.DepartmentFilter
    search_fields = ['duty']
    ordering_fields = ['name']

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


class BuildingViewSet(ModelViewSet):
    queryset = models.Building.objects.all()
    serializer_class = serializers.BuildingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.BuildingFilter
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return [FullDjangoModelPermissions()]
    
    def destroy(self, request, *args, **kwargs):
        if models.Office.objects.filter(department_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Building cannot be deleted because it is associated with office(s)'})
        elif models.ClassRoom.objects.filter(department_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Building cannot be deleted because it is associated with classroom(s)'})
        return super().destroy(request, *args, **kwargs)
    

class OfficeViewSet(ModelViewSet):
    queryset = models.Office.objects.select_related('building').all()
    serializer_class = serializers.OfficeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.OfficeFilter


class EmployeeViewSet(ModelViewSet):
    queryset = models.Employee.objects.select_related('department', 'office', 'person', 'supervisor').all()
    serializer_class = serializers.EmployeeSerializer


class TeacherViewSet(ModelViewSet):
    queryset = models.Teacher.objects.select_related('department', 'office', 'person', 'supervisor').all()
    serializer_class = serializers.TeacherSerializer