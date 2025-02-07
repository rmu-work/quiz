from django.views.generic import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render

from .models import Question
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


class TakeQuizView(LoginRequiredMixin, View):
    template_name = 'take_quiz.html'

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        return render(request, self.template_name, {'quiz': quiz})

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            user_answer = request.POST.get(f'question_{question.id}')

            if question.question_type in ['MCQ', 'TF']:
                correct_option = question.options.filter(is_correct=True).first()
                if correct_option and user_answer == str(correct_option.id):
                    score += 1
            else:  # Short answer
                if user_answer and user_answer.strip().lower() == question.correct_answer.strip().lower():
                    score += 1

        messages.success(request, f'You scored {score} out of {total_questions}!')
        return redirect('quiz_detail', quiz_id=quiz.id)


