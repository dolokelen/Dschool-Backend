from rest_framework import serializers
from . import models

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = ['id', 'name', 'director', 'deputy_director', 'parent', 'budget', 'duty']


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Building
        fields = ['id', 'name', 'care_taker', 'dimension', 'office_counts', 'toilet_counts', 'classroom_counts', 'date_constructed']


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Office
        fields = ['id', 'building', 'dimension']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = ['person', 'first_name', 'last_name','person',
                   'gender', 'phone', 'birth_date', 'religion', 'image', 
                   'relationship', 'status', 'salary', 'department', 
                   'supervisor', 'office', 'job']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['person', 'first_name', 'last_name','person',
                   'gender', 'phone', 'birth_date', 'religion', 'image', 
                   'relationship', 'status', 'salary', 'department', 
                   'supervisor', 'office']