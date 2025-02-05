from django.urls import path
from . import views


urlpatterns = [
    path('quizzes', views.QuizListView.as_view(), name='quizzes'),
    path('quizzes-details/<int:pk>', views.QuizDetailView.as_view(), name='quiz-details'),
]

