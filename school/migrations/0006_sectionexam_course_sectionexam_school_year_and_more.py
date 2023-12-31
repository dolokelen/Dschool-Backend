# Generated by Django 4.2.4 on 2023-08-30 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_attendance_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectionexam',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='exams', to='school.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sectionexam',
            name='school_year',
            field=models.ForeignKey(default=2023, on_delete=django.db.models.deletion.PROTECT, to='school.schoolyear'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sectionexam',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='school.semester'),
            preserve_default=False,
        ),
    ]
