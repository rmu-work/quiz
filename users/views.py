from django.views import View
from django.views.generic import CreateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
import datetime
from django.utils import timezone

from .forms import RegisterForm
from .forms import LoginForm
from .models import User, UserResponse
from quizzes.models import Quiz


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('home')


class LoginView(FormView):
    template_name = "auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.login(self.request)
        return super().form_valid(form)


class Logout(View):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            logout(request)
            return redirect('home')


class TakeQuizView(LoginRequiredMixin, View):
    template_name = 'quiz/take_quiz.html'

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)

        quiz_started, created = UserResponse.objects.get_or_create(
            user=request.user,
            quiz=quiz,
            score=0,
            total_questions=quiz.questions.all().count(),
            is_completed=False
        )
        if created:
            quiz_started.started_at = timezone.now()
            quiz_started.save()
        return render(request, self.template_name, {'quiz': quiz, 'response': quiz_started})

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = 0
        total_questions = quiz.questions.count()

        response_pk = request.POST.get('response_id')

        response = UserResponse.objects.get(pk=response_pk)

        for question in quiz.questions.all():
            correct_answer = question.answers.filter(is_correct=True).first()
            user_answer = request.POST.get(f'question_{question.id}')
            print('question.question_type : ', question.question_type)
            print('user_answer : ', user_answer)
            if question.question_type not in ['TFQ', 'SAQ']:
                print('Entering True/False Question')
                print('type : ', type(question.question_type))
                print('Entering Question')
                user_answer_text = question.answers.filter(pk=user_answer).first()
            else:
                user_answer_text = None

            response_items, created = response.response_details.get_or_create(**{
                'question': question,
                'entered_answer': str(user_answer_text) if user_answer_text else user_answer,
                'correct_answer': correct_answer,
                'is_answered': str(user_answer) is not None,
            })

            if question.question_type == 'TFQ':
                if correct_answer and user_answer.lower() == str(correct_answer).lower():
                    score += 1
                    response_items.is_correct = True
                    response_items.save()
            elif question.question_type == 'MCQ':
                if correct_answer and str(user_answer_text) == str(correct_answer):
                    score += 1
                    response_items.is_correct = True
                    response_items.save()
            else:  # Short answer
                if user_answer and str(user_answer).strip().lower() == str(correct_answer).strip().lower():
                    score += 1
                    response_items.is_correct = True
                    response_items.save()

        response.score = score
        response.ended_at = datetime.datetime.now()
        response.is_completed = True

        messages.success(request, f'You scored {score} out of {total_questions}!')
        return redirect('quiz-result', response_id=response.id)


class QuizResultView(LoginRequiredMixin, View):
    template_name = 'quiz/quiz_result.html'

    def get(self, request, response_id):
        response = get_object_or_404(UserResponse, id=response_id)
        return render(request, self.template_name, {'response': response})
