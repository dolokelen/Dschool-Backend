from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('departments', views.DepartmentViewset)
router.register('buildings', views.BuildingViewSet)
router.register('offices', views.OfficeViewSet)
router.register('employees', views.EmployeeViewSet)
router.register('teachers', views.TeacherViewSet)
router.register('students', views.StudentViewSet)
router.register('majors', views.MajorViewSet)
router.register('student-parents', views.StudentParentViewSet)
router.register('medicals', views.MedicalViewSet)
router.register('scholarships', views.ScholarshipViewSet)
router.register('school-years', views.SchoolYearViewSet)
router.register('catalogs', views.CatalogViewSet)
router.register('text-books', views.TextBookViewSet)
router.register('courses', views.CourseViewSet)
router.register('semester-exams', views.SemesterExamViewSet)
router.register('events', views.EventViewSet)
router.register('semesters', views.SemesterViewSet)
router.register('semester-events', views.SemesterEventViewSet)
router.register('class-rooms', views.ClassRoomViewSet)
router.register('class-times', views.ClassTimeViewSet)
router.register('sections', views.SectionViewSet)
router.register('attendances', views.AttendanceViewSet)
router.register('section-exams', views.SectionExamViewSet)
router.register('teaches', views.TeachViewSet)
router.register('enrollments', views.EnrollmentViewSet)
router.register('grades', views.GradeViewSet)
router.register('supply-categories', views.SupplyCategoryViewSet)
router.register('supplies', views.SupplyViewSet)
# router.register('supply-items', views.SupplyItemViewSet)

urlpatterns = router.urls
# urlpatterns = [
#     path('', )
# ]