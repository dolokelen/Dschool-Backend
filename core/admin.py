from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . models import User, QuizExam

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )


@admin.register(QuizExam)
class QuizExamAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'section', 'question', 'selected_choice']

    