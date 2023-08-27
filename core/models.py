from django.db import models
from django.contrib.auth.models import AbstractUser
from school.models import Course, Student, Section
from evaluation.models import AppraiserChoice, AppraiserQuestion, Choice, QuizQuestion


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, help_text='')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)


class QuizExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quizzes')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='quizzes')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name='quizzes')
    question = models.ForeignKey(QuizQuestion, on_delete=models.PROTECT, related_name='quizzes')
    selected_choice = models.ForeignKey(Choice, on_delete=models.PROTECT, related_name='selectedchoices')    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['question', 'student']]
        
    def __str__(self) -> str:
        return f'{self.student.person.first_name} {self.question} {self.selected_choice}'


class AppraiserResponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='appraiserresponses')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='appraiserresponses')
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name='appraiserresponses')
    question = models.ForeignKey(AppraiserQuestion, on_delete=models.PROTECT, related_name='appraiserresponses')    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['question', 'student']]

    def __str__(self) -> str:
        return f'Response for student {self.student.person}'
    

class AppraiserSelectedChoice(models.Model):
    appraiser_response = models.ForeignKey(AppraiserResponse, on_delete=models.PROTECT, related_name='selectedchoices')
    selected_choice = models.ForeignKey(AppraiserChoice, on_delete=models.PROTECT, related_name='selectedchoices')

    def __str__(self) -> str:
        return f'{self.appraiser_response} - {self.selected_choice}'

