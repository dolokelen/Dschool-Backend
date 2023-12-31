# Generated by Django 4.2.4 on 2023-08-27 02:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppraiserCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppraiserChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='AppraiserQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Published'), ('D', 'Draft')], default='D', max_length=1)),
                ('text', models.CharField(help_text='Question text', max_length=255)),
                ('instruction', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('appraiser_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evaluation.appraisercategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AppraiserResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.CharField(max_length=7)),
                ('end_time', models.CharField(max_length=7)),
                ('week_days', models.CharField(max_length=7)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evaluation.appraiserquestion')),
            ],
        ),
        migrations.CreateModel(
            name='QuizCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Published'), ('D', 'Draft')], default='D', max_length=1)),
                ('text', models.CharField(help_text='Question text', max_length=255)),
                ('instruction', models.CharField(blank=True, max_length=255, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('quiz_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evaluation.quizcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluation.quizquestion')),
            ],
        ),
        migrations.CreateModel(
            name='AppraiserSelectedChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appraiser_response', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evaluation.appraiserresponse')),
                ('selected_choice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evaluation.appraiserchoice')),
            ],
        ),
        migrations.AddField(
            model_name='appraiserresponse',
            name='respondent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evaluation.respondent'),
        ),
        migrations.AddField(
            model_name='appraiserchoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluation.appraiserquestion'),
        ),
        migrations.CreateModel(
            name='QuizExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.CharField(max_length=7)),
                ('end_time', models.CharField(max_length=7)),
                ('week_days', models.CharField(max_length=7)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evaluation.quizquestion')),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluation.respondent')),
                ('selected_choice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evaluation.choice')),
            ],
            options={
                'unique_together': {('respondent', 'question')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='appraiserresponse',
            unique_together={('question', 'respondent')},
        ),
    ]
