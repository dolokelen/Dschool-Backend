# Generated by Django 4.2.4 on 2023-08-30 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_attendance_school_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='school.semester'),
            preserve_default=False,
        ),
    ]
