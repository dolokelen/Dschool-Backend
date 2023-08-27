from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super(PublishedManager, self).get_queryset().filter(status='published')


class QuizCategory(models.Model):
    title = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.title


class AbstractStatusChoice(models.Model):
    PUBLISHED = 'P'
    DRAFT = 'D'
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft')
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT)
    
    class Meta:
        abstract = True


class QuizQuestion(AbstractStatusChoice):
    quiz_category = models.ForeignKey(QuizCategory, on_delete=models.PROTECT)
    text = models.CharField(max_length=255, help_text='Question text')
    instruction = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = models.Manager()  # The default manager
    published = PublishedManager()  # My custom manager

    def __str__(self) -> str:
        return self.text[:15]
    

class Choice(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.label


class Respondent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.user

class QuizExam(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.PROTECT)
    selected_choice = models.ForeignKey(Choice, on_delete=models.PROTECT)
    start_time = models.CharField(max_length=7)
    end_time = models.CharField(max_length=7)
    week_days = models.CharField(max_length=7)    
    date = models.DateTimeField(auto_now_add=True)
   

    class Meta:
        unique_together = [['respondent', 'question']]

    def __str__(self) -> str:
        return f'{self.respondent.user.first_name} {self.question} {self.selected_choice}'
    

class AppraiserCategory(models.Model):
    title = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.title
    

class AppraiserQuestion(AbstractStatusChoice):
    appraiser_category = models.ForeignKey(AppraiserCategory, on_delete=models.PROTECT)
    text = models.CharField(max_length=255, help_text='Question text')
    instruction = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = models.Manager()  # The default manager
    published = PublishedManager()  # My custom manager

    def __str__(self) -> str:
        return self.text
    

class AppraiserChoice(models.Model):
    question = models.ForeignKey(AppraiserQuestion, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.label
    

class AppraiserResponse(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.PROTECT)
    question = models.ForeignKey(AppraiserQuestion, on_delete=models.PROTECT)
    start_time = models.CharField(max_length=7)
    end_time = models.CharField(max_length=7)
    week_days = models.CharField(max_length=7)    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['question', 'respondent']]

    def __str__(self) -> str:
        return self.respondent.user.first_name
    

class AppraiserSelectedChoice(models.Model):
    appraiser_response = models.ForeignKey(AppraiserResponse, on_delete=models.PROTECT)
    selected_choice = models.ForeignKey(AppraiserChoice, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.appraiser_response} - {self.selected_choice}'

