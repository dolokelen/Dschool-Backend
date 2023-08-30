from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.core.exceptions import ValidationError
from school.validators import validate_school_year_at_admin_site


class AbstractStatus(models.Model):
    FULL_TIMER = 'FT'
    PART_TIMER = 'PT'
    STATUS_CHOICES = (
        (FULL_TIMER, 'Full time'),
        (PART_TIMER, 'Part time')
    )
    MARRY = 'M'
    SINGLE = 'S'
    MARIAGE_CHOICES = (
        (MARRY, 'Married'),
        (SINGLE, 'Single')
    )
    relationship = models.CharField(max_length=7, choices=MARIAGE_CHOICES)
    status = models.CharField(
        max_length=5, choices=STATUS_CHOICES, default=PART_TIMER)

    class Meta:
        abstract = True


class Address(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    country = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    community = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.county}, {self.city}, {self.community} '


class Contact(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object_content = GenericForeignKey()
    phone = models.CharField(max_length=25)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.email


class Doucment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    achievement_date = models.DateField()
    institution = models.CharField(
        max_length=255, help_text='Institution name')
    document_type = models.CharField(max_length=200)
    content = models.FileField(upload_to='school/documents')
    rank = models.CharField(
        max_length=50, help_text='e.g: First, Second or Division one')

    def __str__(self) -> str:
        return self.document_type


class Person(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    RELIGION_CHOICES = (
        ('C', 'Christian'),
        ('M', 'Muslim'),
        ('N', 'None')
    )
    person = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    religion = models.CharField(max_length=1, choices=RELIGION_CHOICES)
    phone = models.CharField(max_length=25)
    image = models.ImageField(upload_to='school/images')
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
        # unique_together = [['person', 'image']]

    @admin.display(ordering='person__first_name')
    def first_name(self):
        return self.person.first_name

    @admin.display(ordering='person__last_name')
    def last_name(self):
        return self.person.last_name

    def __str__(self) -> str:
        return f'{self.person.id} - {self.person.first_name}'


class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    director = models.OneToOneField(
        'Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='director')
    deputy_director = models.OneToOneField(
        'Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='deputydirector')
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='departments')
    budget = models.DecimalField(max_digits=8, decimal_places=2)
    duty = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=200, unique=True)
    care_taker = models.ForeignKey(
        'Employee', on_delete=models.PROTECT, null=True, blank=True, related_name='buildings')
    dimension = models.CharField(max_length=200)
    office_counts = models.PositiveSmallIntegerField()
    toilet_counts = models.PositiveSmallIntegerField()
    classroom_counts = models.PositiveSmallIntegerField()
    date_constructed = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Office(models.Model):
    building = models.ForeignKey(
        Building, on_delete=models.PROTECT, related_name='offices')
    dimension = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.building} - {self.id}'


class Employee(AbstractStatus, Person):
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='employees')
    supervisor = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    office = models.ForeignKey(
        Office, on_delete=models.PROTECT, related_name='employees')
    salary = models.DecimalField(max_digits=6, decimal_places=2)
    job = models.TextField(help_text='Description of the employee\'s function')


class Teacher(AbstractStatus, Person):
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='teachers')
    supervisor = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    salary = models.DecimalField(max_digits=6, decimal_places=2)
    office = models.ForeignKey(
        Office, on_delete=models.PROTECT, related_name='teachers')


class Major(models.Model):
    name = models.CharField(max_length=200, unique=True)
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='majors')

    def __str__(self) -> str:
        return f'{self.department} - {self.name}'


class StudentStatus(models.Model):
    FRESHMAN = "FR"
    SOPHOMORE = "SO"
    JUNIOR = "JR"
    SENIOR = "SR"
    GRADUATE = "GR"
    STATUS_CHOICES = (
        (FRESHMAN, "Freshman"),
        (SOPHOMORE, "Sophomore"),
        (JUNIOR, "Junior"),
        (SENIOR, "Senior"),
        (GRADUATE, "Graduate"),
    )
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=FRESHMAN)

    class Meta:
        abstract = True


class Student(StudentStatus, Person):
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name='students')
    supervisor = models.ForeignKey(
        Teacher, on_delete=models.PROTECT, related_name='mentees')
    major = models.ForeignKey(
        Major, on_delete=models.PROTECT, related_name='students')
    registration_fee = models.DecimalField(max_digits=6, decimal_places=2)


class StudentParent(Person):
    OCCUPATION_CHOICES = (
        ('E', 'Employee'),
        ('F', 'Farmer'),
        ('M', 'Business person'),
        ('U', 'Unemploy')
    )
    STUDENT_PARENT_RELATIONSHIP_CHOICES = (
        ('F', 'Father'),
        ('M', 'Mother'),
        ('U', 'Uncle'),
        ('A', 'Aunty'),
        ('B', 'Brother'),
        ('S', 'Sister'),
        ('O', 'Other')
    )
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    occupation = models.CharField(max_length=1, choices=OCCUPATION_CHOICES)
    relationship_to_student = models.CharField(
        max_length=1, choices=STUDENT_PARENT_RELATIONSHIP_CHOICES)


class Medical(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='medicals')
    document_name = models.CharField(max_length=255)
    certificate = models.FileField(
        upload_to='school/medicals', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    medical_center_name = models.CharField(max_length=255)
    date_issued = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.student}-{self.document_name}'


class Scholarship(models.Model):
    SPONSOR_CHOICES = (
        ('G', 'Government'),
        ('P', 'Private')
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scholarships')
    name = models.CharField(max_length=255)
    sponsor_name = models.CharField(max_length=255)
    scholarship_type = models.CharField(max_length=1, choices=SPONSOR_CHOICES)
    is_full = models.BooleanField(default=False)
    document = models.FileField(upload_to='school/scholarships',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    date_issued = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class SchoolYear(models.Model):
    year = models.PositiveIntegerField(primary_key=True, validators=[validate_school_year_at_admin_site])

    def __str__(self) -> str:
        return str(self.year)


class Catalog(models.Model):
    title = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.title


class TextBook(models.Model):
    title = models.CharField(max_length=150, unique=True)
    catalog = models.ForeignKey(
        Catalog, on_delete=models.PROTECT, related_name='books')
    file = models.FileField(upload_to='school/books',
                            validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    author = models.CharField(max_length=255)
    subject = models.CharField(
        max_length=255, help_text='e.g: English, Mathematics')
    price = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, help_text='Amount spent to purchase.')
    publisher = models.CharField(max_length=255)
    published_date = models.DateField()
    edition = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Course(StudentStatus):
    code = models.CharField(max_length=50, unique=True)
    prerequisite = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='prerequisites')
    books = models.ManyToManyField(
        TextBook, blank=True, related_name='courses')
    title = models.CharField(max_length=200, unique=True)
    syllabus = models.FileField(
        upload_to='school/syllabus', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    objective = models.FileField(
        upload_to='school/books', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    price_per_credit = models.DecimalField(max_digits=5, decimal_places=2)
    credit = models.PositiveSmallIntegerField()
    additional_fee = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.code


class SemesterExam(models.Model):
    name = models.CharField(max_length=200, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self) -> str:
        return self.name


class Semester(models.Model):
    NAME_CHOICES = (
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III')
    )
    name = models.CharField(max_length=3, choices=NAME_CHOICES)
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.PROTECT, related_name='semesters')
    courses = models.ManyToManyField(Course, related_name='semesters')
    conducted_exams = models.ManyToManyField(
        SemesterExam, related_name='semesters')
    enrollment_start_date = models.DateField()
    enrollment_end_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    program_overview = models.FileField(upload_to='school/semester-programs', validators=[
                                        FileExtensionValidator(allowed_extensions=['pdf'])])

    class Meta:
        unique_together = [['name', 'school_year']]

    def __str__(self) -> str:
        return self.name


class SemesterEvent(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT, related_name='semesters')
    semester = models.ForeignKey(
        Semester, on_delete=models.PROTECT, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.semester.name} {self.event.name}'


class ClassRoom(models.Model):
    building = models.ForeignKey(
        Building, on_delete=models.PROTECT, related_name='classrooms')
    name = models.CharField(max_length=200, unique=True)
    dimension = models.CharField(max_length=200)
    create_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = [['building', 'name']]

    def __str__(self) -> str:
        return f'{self.building}-{self.name}'


class AbstractPositiveIntegerField(models.Model):
    start_hour = models.CharField(max_length=2)
    start_minute = models.CharField(max_length=4)
    end_hour = models.CharField(max_length=2)
    end_minute = models.CharField(max_length=4)
    week_days = models.CharField(max_length=7)

    class Meta:
        abstract = True


class ClassTime(AbstractPositiveIntegerField):
    class Meta:
        unique_together = [['start_hour', 'start_minute',
                            'end_hour', 'end_minute', 'week_days']]

    def __str__(self) -> str:
        return f'{self.start_hour}:{self.start_minute}-{self.end_hour}:{self.end_minute} {self.week_days}'


class Section(models.Model):
    name = models.PositiveSmallIntegerField(validators=[MinValueValidator(1, message='Section name cannot be less than 1!')])
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name='sections')
    classroom = models.ForeignKey(
        ClassRoom, on_delete=models.PROTECT, related_name='sections')
    classtime = models.ForeignKey(
        ClassTime, on_delete=models.PROTECT, related_name='sections')

    class Meta:
        unique_together = [['classroom', 'classtime']]

    def __str__(self) -> str:
        return str(self.name)


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
        ('E', 'Excuse'),
        ('T', 'Tardy')
    )
    student = models.ForeignKey(
        Student, on_delete=models.PROTECT, related_name='attendance')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='attendance')
    section = models.ForeignKey(
        Section, on_delete=models.PROTECT, related_name='attendance')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.student.person.first_name


class SectionExam(AbstractPositiveIntegerField):
    name = models.CharField(max_length=200, unique=True, help_text='Exam name')
    classroom = models.ForeignKey(
        ClassRoom, on_delete=models.PROTECT, related_name='exams')
    sections = models.ManyToManyField(Section, related_name='exams')

    class Meta:
        unique_together = [['classroom', 'start_hour',
                            'start_minute', 'end_hour', 'end_minute', 'week_days']]

    def __str__(self) -> str:
        return self.name


class Teach(models.Model):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.PROTECT, related_name='teaches')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='teaches')
    section = models.ForeignKey(
        Section, on_delete=models.PROTECT, related_name='teaches')
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT, related_name='teaches')
    semester = models.ForeignKey(
        Semester, on_delete=models.PROTECT, related_name='teaches')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['teacher', 'course', 'section']]

    def __str__(self) -> str:
        return self.teacher.person.first_name


class Enrollment(models.Model):
    APPROVED = 'A'
    PENDING = 'P'
    CANCELLED = 'C'
    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (CANCELLED, 'Cancelled')
    )
    student = models.ForeignKey(
        Student, on_delete=models.PROTECT, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='enrollments')
    section = models.ForeignKey(
        Section, on_delete=models.PROTECT, related_name='enrollments')
    semester = models.ForeignKey(
        Semester, on_delete=models.PROTECT, related_name='enrollments')
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT, related_name='enrollments')
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['student', 'course', 'section']]

    def __str__(self) -> str:
        return f'{self.student.person.first_name} {self.course.code} section {str(self.section.name)}'


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='grades')
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT, related_name='grades')
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='grades')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name='grades')
    attendance = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10, message='Points cannot be grater than 10!')])
    quiz = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10, message='Points cannot be grater than 10!')])
    assignment = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5, message='Points cannot be grater than 5!')])
    midterm = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(25, message='Points cannot be grater than 25!')])
    project = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(15, message='Points cannot be grater than 15!')])
    final = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(35, message='Points cannot be grater than 35!')])
    date_assigned = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Grade for {self.student.person.first_name}'
    

class SupplyCategory(models.Model):
    title = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.title


class Supply(models.Model):
    supply_category = models.ForeignKey(SupplyCategory, on_delete=models.PROTECT, related_name='supplies')
    name = models.CharField(max_length=255, unique=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(1, message='Price cannot be less than $1')])
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class SupplyItem(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.PROTECT, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='supplyitems')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1, message='Quantity cannot be less than 1!')])

    class Meta:
        unique_together = [['supply', 'content_type', 'object_id']]
    
    def clean(self):
        if self._state.adding and self.supply and self.quantity > self.supply.quantity:
            raise ValidationError(f"{self.supply.name} current quantity ({self.supply.quantity}) is lower than {self.quantity}")

    #(When supply is 0, and you trying increasing supplyitem it crashes)
    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
            self.supply.quantity -= self.quantity
            self.supply.save()
        else:
            old_item = SupplyItem.objects.get(pk=self.pk)
            quantity_diff = old_item.quantity - self.quantity
            self.supply.quantity += quantity_diff
            super().save(*args, **kwargs)
            self.supply.save()

    def __str__(self) -> str:
        return self.supply.name




