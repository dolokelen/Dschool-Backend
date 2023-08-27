# Generated by Django 4.2.4 on 2023-08-27 02:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('dimension', models.CharField(max_length=200)),
                ('office_counts', models.PositiveSmallIntegerField()),
                ('toilet_counts', models.PositiveSmallIntegerField()),
                ('classroom_counts', models.PositiveSmallIntegerField()),
                ('date_constructed', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('dimension', models.CharField(max_length=200)),
                ('create_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='classrooms', to='school.building')),
            ],
            options={
                'unique_together': {('building', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ClassTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_hour', models.CharField(max_length=2)),
                ('start_minute', models.CharField(max_length=4)),
                ('end_hour', models.CharField(max_length=2)),
                ('end_minute', models.CharField(max_length=4)),
                ('week_days', models.CharField(max_length=7)),
            ],
            options={
                'unique_together': {('start_hour', 'start_minute', 'end_hour', 'end_minute', 'week_days')},
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate')], default='FR', max_length=2)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('syllabus', models.FileField(upload_to='school/syllabus', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('objective', models.FileField(upload_to='school/books', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('price_per_credit', models.DecimalField(decimal_places=2, max_digits=5)),
                ('credit', models.PositiveSmallIntegerField()),
                ('additional_fee', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=8)),
                ('duty', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='majors', to='school.department')),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dimension', models.CharField(max_length=200)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='offices', to='school.building')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('year', models.PositiveIntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Section name cannot be less than 1!')])),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='school.classroom')),
                ('classtime', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='school.classtime')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='school.course')),
            ],
            options={
                'unique_together': {('classroom', 'classtime')},
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('I', 'I'), ('II', 'II'), ('III', 'III')], max_length=3)),
                ('enrollment_start_date', models.DateField()),
                ('enrollment_end_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('program_overview', models.FileField(upload_to='school/semester-programs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
            ],
        ),
        migrations.CreateModel(
            name='SemesterExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('religion', models.CharField(choices=[('C', 'Christian'), ('M', 'Muslim'), ('N', 'None')], max_length=1)),
                ('phone', models.CharField(max_length=25)),
                ('image', models.ImageField(upload_to='school/images')),
                ('joined_at', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate')], default='FR', max_length=2)),
                ('registration_fee', models.DecimalField(decimal_places=2, max_digits=6)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='students', to='school.department')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='students', to='school.major')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TextBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('file', models.FileField(upload_to='school/books', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('author', models.CharField(max_length=255)),
                ('subject', models.CharField(help_text='e.g: English, Mathematics', max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, help_text='Amount spent to purchase.', max_digits=5)),
                ('publisher', models.CharField(max_length=255)),
                ('published_date', models.DateField()),
                ('edition', models.CharField(max_length=50)),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='school.catalog')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('relationship', models.CharField(choices=[('M', 'Married'), ('S', 'Single')], max_length=7)),
                ('status', models.CharField(choices=[('FT', 'Full time'), ('PT', 'Part time')], default='PT', max_length=5)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('religion', models.CharField(choices=[('C', 'Christian'), ('M', 'Muslim'), ('N', 'None')], max_length=1)),
                ('phone', models.CharField(max_length=25)),
                ('image', models.ImageField(upload_to='school/images')),
                ('joined_at', models.DateField(auto_now_add=True)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=6)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teachers', to='school.department')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teachers', to='school.office')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinates', to='school.teacher')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(1, message='Price cannot be less than $1')])),
                ('comment', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('supply_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supplies', to='school.supplycategory')),
            ],
        ),
        migrations.CreateModel(
            name='StudentParent',
            fields=[
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('religion', models.CharField(choices=[('C', 'Christian'), ('M', 'Muslim'), ('N', 'None')], max_length=1)),
                ('phone', models.CharField(max_length=25)),
                ('image', models.ImageField(upload_to='school/images')),
                ('joined_at', models.DateField(auto_now_add=True)),
                ('occupation', models.CharField(choices=[('E', 'Employee'), ('F', 'Farmer'), ('M', 'Business person'), ('U', 'Unemploy')], max_length=1)),
                ('relationship_to_student', models.CharField(choices=[('F', 'Father'), ('M', 'Mother'), ('U', 'Uncle'), ('A', 'Aunty'), ('B', 'Brother'), ('S', 'Sister'), ('O', 'Other')], max_length=1)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='school.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='student',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mentees', to='school.teacher'),
        ),
        migrations.CreateModel(
            name='SemesterEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='semesters', to='school.event')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='events', to='school.semester')),
            ],
        ),
        migrations.AddField(
            model_name='semester',
            name='conducted_exams',
            field=models.ManyToManyField(related_name='semesters', to='school.semesterexam'),
        ),
        migrations.AddField(
            model_name='semester',
            name='courses',
            field=models.ManyToManyField(related_name='semesters', to='school.course'),
        ),
        migrations.AddField(
            model_name='semester',
            name='school_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='semesters', to='school.schoolyear'),
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sponsor_name', models.CharField(max_length=255)),
                ('scholarship_type', models.CharField(choices=[('G', 'Government'), ('P', 'Private')], max_length=1)),
                ('is_full', models.BooleanField(default=False)),
                ('document', models.FileField(upload_to='school/scholarships', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('date_issued', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scholarships', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Medical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(max_length=255)),
                ('certificate', models.FileField(upload_to='school/medicals', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('medical_center_name', models.CharField(max_length=255)),
                ('date_issued', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicals', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10, message='Points cannot be grater than 10!')])),
                ('quiz', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10, message='Points cannot be grater than 10!')])),
                ('assignment', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5, message='Points cannot be grater than 5!')])),
                ('midterm', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(25, message='Points cannot be grater than 25!')])),
                ('project', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(15, message='Points cannot be grater than 15!')])),
                ('final', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(35, message='Points cannot be grater than 35!')])),
                ('date_assigned', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grades', to='school.course')),
                ('school_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grades', to='school.schoolyear')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grades', to='school.section')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grades', to='school.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grades', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('relationship', models.CharField(choices=[('M', 'Married'), ('S', 'Single')], max_length=7)),
                ('status', models.CharField(choices=[('FT', 'Full time'), ('PT', 'Part time')], default='PT', max_length=5)),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('religion', models.CharField(choices=[('C', 'Christian'), ('M', 'Muslim'), ('N', 'None')], max_length=1)),
                ('phone', models.CharField(max_length=25)),
                ('image', models.ImageField(upload_to='school/images')),
                ('joined_at', models.DateField(auto_now_add=True)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=6)),
                ('job', models.TextField(help_text="Description of the employee's function")),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='school.department')),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='school.office')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subordinates', to='school.employee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Doucment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('achievement_date', models.DateField()),
                ('institution', models.CharField(help_text='Institution name', max_length=255)),
                ('document_type', models.CharField(max_length=200)),
                ('content', models.FileField(upload_to='school/documents')),
                ('rank', models.CharField(help_text='e.g: First, Second or Division one', max_length=50)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='deputy_director',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deputydirector', to='school.employee'),
        ),
        migrations.AddField(
            model_name='department',
            name='director',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='director', to='school.employee'),
        ),
        migrations.AddField(
            model_name='department',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departments', to='school.department'),
        ),
        migrations.AddField(
            model_name='course',
            name='books',
            field=models.ManyToManyField(blank=True, related_name='courses', to='school.textbook'),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prerequisites', to='school.course'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('phone', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.AddField(
            model_name='building',
            name='care_taker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='buildings', to='school.employee'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('E', 'Excuse'), ('T', 'Tardy')], max_length=1)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attendance', to='school.section')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attendance', to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('country', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('community', models.CharField(max_length=200)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Teach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teaches', to='school.course')),
                ('school_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teaches', to='school.schoolyear')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teaches', to='school.section')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teaches', to='school.semester')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teaches', to='school.teacher')),
            ],
            options={
                'unique_together': {('teacher', 'course', 'section')},
            },
        ),
        migrations.CreateModel(
            name='SupplyItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Quantity cannot be less than 1!')])),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplyitems', to='contenttypes.contenttype')),
                ('supply', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='school.supply')),
            ],
            options={
                'unique_together': {('supply', 'content_type', 'object_id')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together={('name', 'school_year')},
        ),
        migrations.CreateModel(
            name='SectionExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_hour', models.CharField(max_length=2)),
                ('start_minute', models.CharField(max_length=4)),
                ('end_hour', models.CharField(max_length=2)),
                ('end_minute', models.CharField(max_length=4)),
                ('week_days', models.CharField(max_length=7)),
                ('name', models.CharField(help_text='Exam name', max_length=200, unique=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exams', to='school.classroom')),
                ('sections', models.ManyToManyField(related_name='exams', to='school.section')),
            ],
            options={
                'unique_together': {('classroom', 'start_hour', 'start_minute', 'end_hour', 'end_minute', 'week_days')},
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Approved'), ('P', 'Pending'), ('C', 'Cancelled')], default='P', max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enrollments', to='school.course')),
                ('school_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enrollments', to='school.schoolyear')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enrollments', to='school.section')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enrollments', to='school.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enrollments', to='school.student')),
            ],
            options={
                'unique_together': {('student', 'course', 'section')},
            },
        ),
    ]
