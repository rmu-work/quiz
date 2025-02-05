from django.views.generic import DetailView
from django.views.generic import ListView
from django.urls import reverse_lazy

from .models import Quiz


class QuizListView(ListView):
    model = Quiz
    context_object_name = 'quizzes'
    template_name = 'quiz/quiz_list.html'
    paginate_by = 10
    ordering = ['-created_at']


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'
    context_object_name = 'quiz'



