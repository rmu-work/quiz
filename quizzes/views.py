from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Quiz


class QuizListView(ListView):
    model = Quiz
    queryset = Quiz.objects.filter(is_published=True)  # Fetch all quizzes instead of all objects in the database
    context_object_name = 'quizzes'
    template_name = 'quiz_list.html'
    paginate_by = 10
    ordering = ['-created_at']


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz_detail.html'
    context_object_name = 'quiz'
