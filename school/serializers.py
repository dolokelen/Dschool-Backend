from rest_framework import serializers
from . import models

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = ['id', 'name', 'director', 'deputy_director', 'parent', 'budget', 'duty']


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Building
        fields = ['id', 'name', 'care_taker', 'dimension', 'office_counts', 
                  'toilet_counts', 'classroom_counts', 'date_constructed']


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Office
        fields = ['id', 'building', 'dimension']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = ['person', 'first_name', 'last_name', 'gender', 'phone', 
                  'birth_date', 'religion', 'image', 'relationship', 'status', 
                  'salary', 'department', 'supervisor', 'office', 'job']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['person', 'first_name', 'last_name', 'gender', 
                  'phone', 'birth_date', 'religion', 'image', 'relationship', 
                  'status', 'salary', 'department', 'supervisor', 'office']


class StudentParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentParent
        fields = ['person', 'student', 'first_name', 'last_name',
                'gender', 'phone', 'birth_date', 'religion', 'image', 
                'occupation', 'relationship_to_student']
        

class MedicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medical
        fields = ['id', 'student', 'document_name', 'certificate', 
                  'medical_center_name', 'date_issued']


class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Scholarship
        fields = ['id', 'student', 'name', 'sponsor_name', 
                  'scholarship_type', 'is_full', 'document', 'date_issued']
        
class StudentSerializer(serializers.ModelSerializer):
    studentparent_set = StudentParentSerializer(many=True, read_only=True)
    medicals = MedicalSerializer(many=True, read_only=True)
    scholarships = ScholarshipSerializer(many=True, read_only=True)
    class Meta:
        model = models.Student
        fields = ['person', 'first_name', 'last_name', 'gender', 
                  'phone', 'birth_date', 'religion', 'image', 'major', 
                  'registration_fee', 'status', 'department', 'supervisor', 
                  'medicals', 'studentparent_set', 'scholarships']
        

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Major
        fields = ['id', 'name', 'department']


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SchoolYear
        fields = ['year']


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Catalog
        fields = ['id', 'title']


class TextBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextBook
        fields = ['id', 'catalog', 'title', 'subject', 'file', 'edition', 
                  'price', 'author', 'publisher', 'published_date']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'code', 'prerequisite', 'books', 'title', 'syllabus', 
                  'objective', 'price_per_credit', 'credit', 'additional_fee']


class SemesterExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SemesterExam
        fields = ['id', 'name', 'start_date', 'end_date']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ['id', 'name', 'start_date', 'end_date']


class SemesterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SemesterEvent
        fields = ['id', 'semester', 'event']

class SimpleSemesterEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SemesterEvent
        fields = ['id', 'event']


class SemesterSerializer(serializers.ModelSerializer):
    events = SimpleSemesterEventSerializer(many=True, read_only=True)
    class Meta:
        model = models.Semester
        fields = ['id', 'name', 'school_year', 'courses', 'conducted_exams', 
                  'enrollment_start_date', 'enrollment_end_date', 'start_date', 
                  'end_date', 'program_overview', 'events']

class UpdateSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Semester
        fields = ['name', 'school_year', 'courses', 'conducted_exams', 
                  'enrollment_start_date', 'enrollment_end_date', 'start_date', 
                  'end_date']
        

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClassRoom
        fields = ['id', 'building', 'name', 'dimension']


class ClassTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClassTime
        fields = ['id', 'start_hour', 'start_minute', 'end_hour', 'end_minute', 'week_days']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Section
        fields = ['id', 'name', 'course', 'classroom', 'classtime']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attendance
        fields = ['id', 'student', 'section', 'course', 'classroom', 'classtime']




