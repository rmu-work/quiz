from django.db import models
from home.middleware.request import CurrentRequestMiddleware


class Quiz(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    category = models.ForeignKey('masterdata.Category', on_delete=models.CASCADE, verbose_name='Category', related_name='quiz_category')
    description = models.TextField(blank=True, null=True, verbose_name='description')
    time_limit = models.IntegerField(help_text="Time limit in minutes", null=True, blank=True, verbose_name='Time Limit')
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Created By')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        _request = CurrentRequestMiddleware.get_request()
        user = _request.user if _request else None
        if user and self.id is None:
            self.created_by = user

        super().save(*args, **kwargs)


class Question(models.Model):
    QUESTION_TYPE = [
        ('MCQ', 'Multiple Choice'),
        ('TFQ', 'True/False'),
        ('SAQ', 'Short Answer'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Quiz', related_name='questions')
    text = models.CharField(max_length=255, verbose_name='Text')
    question_type = models.CharField(max_length=255, choices=QUESTION_TYPE, verbose_name='Question Type')

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question', related_name='answers')
    text = models.CharField(max_length=255, verbose_name='Text')
    is_correct = models.BooleanField(default=False, verbose_name='Is Correct')
    order = models.PositiveIntegerField(default=1, verbose_name='Order')

    def __str__(self):
        return self.text

