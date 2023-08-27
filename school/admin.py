from typing import Any
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models


class AddressInline(GenericStackedInline):
    model = models.Address
    extra = 1


class ContactInline(GenericStackedInline):
    model = models.Contact
    extra = 1


class DocumentInline(GenericStackedInline):
    model = models.Doucment
    extra = 1


class SupplyItemInline(GenericStackedInline):
    model = models.SupplyItem
    extra = 1

@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [AddressInline, ContactInline, SupplyItemInline]
    search_fields = ['name']
    autocomplete_fields = ['director', 'deputy_director', 'parent']
    list_display = ['name', 'director', 'deputy_director', 'budget', 'parent','duty']



@admin.register(models.Office)
class OfficeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['building']
    search_fields = ['building']
    list_select_related = ['building']
    list_display = ['building', 'dimension']

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [DocumentInline, AddressInline, ContactInline]
    search_fields = ['person.username']
    autocomplete_fields = ['person', 'department', 'supervisor', 'office']
    list_select_related = ['department', 'office']
    list_display = ['first_name', 'last_name', 'department', 'supervisor', 'office', 'job']


@admin.register(models.Building)
class BuildingAdmin(admin.ModelAdmin):
    inlines = [AddressInline]
    search_fields = ['name']
    list_select_related = ['care_taker']
    list_display = ['name', 'care_taker', 'dimension', 'office_counts', 'toilet_counts', 'classroom_counts', 'date_constructed']


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [DocumentInline, AddressInline, ContactInline]
    search_fields = ['first_name']
    autocomplete_fields = ['person', 'supervisor']
    list_select_related = ['department', 'office']
    list_display = ['first_name', 'last_name', 'department', 'supervisor','salary', 'office']


@admin.register(models.Major)
class MajorAdmin(admin.ModelAdmin):
    autocomplete_fields = ['department']
    list_select_related = ['department']
    search_fields = ['name']
    list_display = ['name', 'department']


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [DocumentInline, AddressInline, ContactInline]
    autocomplete_fields = ['person', 'department', 'supervisor', 'major']
    list_select_related = ['department', 'supervisor', 'major']
    search_fields = ['first_name']
    list_display = ['first_name', 'last_name', 'department', 'major', 'registration_fee']

@admin.register(models.StudentParent)
class StudentParentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['student', 'person']
    list_select_related = ['student']
    inlines = [AddressInline, ContactInline]
    list_display = ['first_name', 'student', 'relationship_to_student', 'occupation']


@admin.register(models.Medical)
class MedicalAdmin(admin.ModelAdmin):
    list_select_related = ['student']
    autocomplete_fields = ['student']
    list_display = ['document_name', 'medical_center_name', 'student', 'date_issued', 'certificate']


@admin.register(models.Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    inlines = [AddressInline, ContactInline]
    autocomplete_fields = ['student']
    list_display = ['student', 'name', 'sponsor_name', 'scholarship_type', 'is_full', 'document', 'date_issued']


@admin.register(models.SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    search_fields = ['year']
    list_display = ['year']


@admin.register(models.Catalog)
class CatalogAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']
    

@admin.register(models.TextBook)
class TextBookAdmin(admin.ModelAdmin):
    list_select_related = ['catalog']
    autocomplete_fields = ['catalog']
    search_fields = ['title']
    list_display = ['title', 'subject', 'catalog', 'file', 'price', 'publisher', 'published_date']


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['code']
    autocomplete_fields = ['books']
    list_display = ['code', 'title', 'prerequisite', 'price_per_credit', 'credit','additional_fee', 'objective', 'syllabus']


@admin.register(models.SemesterExam)
class SemesterExamAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'start_date', 'end_date']


@admin.register(models.Event)
class EvantAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'start_date', 'end_date']


@admin.register(models.Semester)
class SemesterAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['courses', 'conducted_exams']
    list_display = ['name', 'school_year', 'enrollment_start_date', 'enrollment_end_date', 'start_date', 'end_date', 'program_overview']


@admin.register(models.SemesterEvent)
class SemesterEventAdmin(admin.ModelAdmin):
    autocomplete_fields = ['event', 'semester']
    list_select_related = ['event', 'semester']
    list_display = ['event', 'semester']


@admin.register(models.ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    autocomplete_fields = ['building']
    search_fields = ['name']
    list_display = ['name', 'dimension', 'building']


@admin.register(models.ClassTime)
class ClassTimeAdmin(admin.ModelAdmin):
    search_fields = ['start_hour', 'start_minute', 'end_hour', 'end_minute', 'week_days']
    list_display = ['start_hour', 'start_minute', 'end_hour', 'end_minute', 'week_days']


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['course', 'classroom', 'classtime']
    list_select_related = ['course', 'classroom', 'classtime']
    list_display = ['name', 'course', 'classroom', 'classtime']


@admin.register(models.Attendance)
class AddentanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['student', 'section']
    list_select_related = ['student', 'section']
    list_display = ['student', 'section', 'status', 'comment']


@admin.register(models.Teach)
class TeachAdmin(admin.ModelAdmin):
    autocomplete_fields = ['section', 'teacher', 'semester']
    list_select_related = ['teacher', 'section', 'semester']
    list_display = ['teacher', 'section', 'semester']


@admin.register(models.Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    search_fields = ['section', 'school_year']
    autocomplete_fields = ['student', 'section', 'semester']
    list_select_related = ['student', 'section', 'semester']
    list_display = ['student', 'section', 'school_year', 'semester', 'status']


@admin.register(models.Grade)
class GradeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['student', 'semester', 'school_year', 'course', 'section']
    list_display = ['student', 'school_year', 'semester', 'course', 'section', 'attendance', 'quiz', 'assignment', 'midterm', 'project', 'final']


@admin.register(models.SupplyCategory)
class SupplyCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']


@admin.register(models.Supply)
class SupplyAdmin(admin.ModelAdmin):
    autocomplete_fields = ['supply_category']
    list_display = ['name', 'supply_category', 'quantity', 'unit_price', 'comment']

