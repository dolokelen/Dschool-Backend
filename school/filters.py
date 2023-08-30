from django_filters.rest_framework import FilterSet
from . import models

class OfficeFilter(FilterSet):
    class Meta:
        model = models.Office
        fields = {
            'building_id': ['exact'],        
        }


class BuildingFilter(FilterSet):
    class Meta:
        model = models.Building
        fields = {
            'name': ['exact'],        
        }

class DepartmentFilter(FilterSet):
    class Meta:
        model = models.Department
        fields = {
            'name': ['exact'],        
        }
