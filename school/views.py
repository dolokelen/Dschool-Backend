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


class StudentViewSet(ModelViewSet):
    queryset = models.Student.objects.select_related('department', 'major', 'person', 'supervisor')\
        .prefetch_related('studentparent_set', 'medicals', 'scholarships').all()
    serializer_class = serializers.StudentSerializer


class MajorViewSet(ModelViewSet):
    queryset = models.Major.objects.select_related('department').all()
    serializer_class = serializers.MajorSerializer


class StudentParentViewSet(ModelViewSet):
    queryset = models.StudentParent.objects.select_related('student').all()
    serializer_class = serializers.StudentParentSerializer


class MedicalViewSet(ModelViewSet):
    queryset = models.Medical.objects.select_related('student').all()
    serializer_class = serializers.MedicalSerializer


class ScholarshipViewSet(ModelViewSet):
    queryset = models.Medical.objects.select_related('student').all()
    serializer_class = serializers.ScholarshipSerializer


class SchoolYearViewSet(ModelViewSet):
    queryset = models.SchoolYear.objects.all()
    serializer_class = serializers.SchoolYearSerializer


class CatalogViewSet(ModelViewSet):
    queryset = models.Catalog.objects.all()
    serializer_class = serializers.CatalogSerializer


class TextBookViewSet(ModelViewSet):
    queryset = models.TextBook.objects.select_related('catalog').all()
    serializer_class = serializers.TextBookSerializer


class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.select_related('prerequisite').prefetch_related('books').all()
    serializer_class = serializers.CourseSerializer


class SemesterExamViewSet(ModelViewSet):
    queryset = models.SemesterExam.objects.all()
    serializer_class = serializers.SemesterExamSerializer


class EventViewSet(ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class SemesterViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'option']
    queryset = models.Semester.objects.select_related('school_year')\
        .prefetch_related('courses', 'conducted_exams', 'events').all()
    serializer_class = serializers.SemesterSerializer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return serializers.UpdateSemesterSerializer
        return serializers.SemesterSerializer
    

class SemesterEventViewSet(ModelViewSet):
    queryset = models.SemesterEvent.objects.select_related('semester', 'event').all()
    serializer_class = serializers.SemesterEventSerializer
        

class ClassRoomViewSet(ModelViewSet):
    queryset = models.ClassRoom.objects.select_related('building').all()
    serializer_class = serializers.ClassRoomSerializer

class ClassTimeViewSet(ModelViewSet):
    queryset = models.ClassTime.objects.all()
    serializer_class = serializers.ClassTimeSerializer


class SectionViewSet(ModelViewSet):
    queryset = models.Section.objects.select_related('course', 'classroom', 'classtime').all()
    serializer_class = serializers.SectionSerializer









