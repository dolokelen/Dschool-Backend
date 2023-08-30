from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('departments', views.DepartmentViewset)
router.register('buildings', views.BuildingViewSet)
router.register('offices', views.OfficeViewSet)
router.register('employees', views.EmployeeViewSet)
router.register('teachers', views.TeacherViewSet)

urlpatterns = router.urls
# urlpatterns = [
#     path('', )
# ]