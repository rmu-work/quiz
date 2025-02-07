from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Quiz


class QuizListView(ListView):
    model = Quiz
    context_object_name = 'quizzes'
    template_name = 'quiz_list.html'
    paginate_by = 10
    ordering = ['-created_at']


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz_detail.html'
    context_object_name = 'quiz'
