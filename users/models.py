from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=150, null=True, verbose_name='Name')
    mobile_number = models.CharField(max_length=25, null=True, verbose_name='Mobile Number')

    def __str__(self):
        return self.name or self.username


class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='response')
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE, verbose_name='Quiz', related_name='attended_quiz')
    score = models.PositiveIntegerField(verbose_name='Score', blank=True, null=True)
    started_at = models.DateTimeField(verbose_name='Started At', blank=True, null=True)
    ended_at = models.DateTimeField(verbose_name='Ended At', blank=True, null=True)
    total_questions = models.PositiveIntegerField(verbose_name='Total Questions', blank=True, null=True)
    is_completed = models.BooleanField(default=False, verbose_name='Completed')

    def __str__(self):
        return f"{self.user} - {self.quiz}"


class QuestionAnswers(models.Model):
    user_response = models.ForeignKey(
        UserResponse, on_delete=models.CASCADE, verbose_name='User Response', related_name='response_details'
    )
    question = models.ForeignKey(
        'quizzes.Question', on_delete=models.CASCADE, verbose_name='Question', related_name='answered_question'
    )
    entered_answer = models.TextField(verbose_name='Entered Answer')
    correct_answer = models.ForeignKey(
        'quizzes.Answer', on_delete=models.CASCADE, verbose_name='Correct Answer', related_name='correct_answer'
    )
    is_answered = models.BooleanField(default=False, verbose_name='Is Correct')
    is_correct = models.BooleanField(default=False, verbose_name='Is Correct')

    def __str__(self):
        return f"{self.user_response} - {self.question}"

