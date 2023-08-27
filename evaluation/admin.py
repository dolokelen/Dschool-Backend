from django.contrib import admin
from . import models


class ChoiceInline(admin.StackedInline):
    model = models.Choice
    extra = 1

@admin.register(models.QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']


@admin.register(models.QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    autocomplete_fields = ['quiz_category']
    list_display = ['quiz_category', 'text', 'status']


class AppraiserChoiceInline(admin.StackedInline):
    model = models.AppraiserChoice
    extra = 1

@admin.register(models.AppraiserCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']


@admin.register(models.AppraiserQuestion)
class AppraiserQuestionAdmin(admin.ModelAdmin):
    inlines = [AppraiserChoiceInline]
    autocomplete_fields = ['appraiser_category']
    list_display = ['appraiser_category', 'text', 'status']
    
