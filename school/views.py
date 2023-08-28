from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers


class DepartmentViewset(ModelViewSet):
    serializer_class = serializers.DepartmentSerializer
    queryset = models.Department.objects.all()
