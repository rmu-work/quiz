from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logot/', views.Logout.as_view(), name='logout'),
    path('quizzes/take-quiz/<int:quiz_id>/', views.TakeQuizView.as_view(), name='take-quiz'),
    path('quizzes/result/<int:response_id>/', views.QuizResultView.as_view(), name='quiz-result'),
]

