from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render
from django.urls import path

from .models import Quiz
from .models import Question
from .models import Answer

from .forms import QuizModelForm
from .forms import AnswerModelForm


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'category', 'created_at', 'created_by',)
    readonly_fields = ('created_at', 'created_by',)
    search_fields = ('title', 'category__name',)
    search_help_text = 'Search with title and category name'
    list_filter = ('category', 'created_at',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'description', 'time_limit',)
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('title', 'category', 'description', 'time_limit',)
        }),
    )
    form = QuizModelForm
    actions = ['publish_quiz']

    def publish_quiz(self, request, queryset):
        # If this is a POST request with confirmation
        if request.POST.get('post') == 'yes':
            error_count = 0
            failed_quizzes = set()

            for quiz in queryset:
                try:
                    # Validate questions exist
                    questions = quiz.questions.all()
                    if not questions.exists():
                        raise ValueError(f"Quiz '{quiz.title}' has no questions.")

                    # Validate each question
                    for question in questions:
                        answers = question.answers.all()
                        correct_answers = answers.filter(is_correct=True)

                        if question.question_type != 'MCQ':
                            if correct_answers.count() != 1:
                                raise ValueError(
                                    f"Quiz '{quiz.title}': {question.question_type} question must have exactly 1 correct answer."
                                )
                        else:
                            if correct_answers.count() < 1:
                                raise ValueError(
                                    f"Quiz '{quiz.title}': MCQ question must have at least 1 correct answer."
                                )
                            if answers.count() < 2:
                                raise ValueError(
                                    f"Quiz '{quiz.title}': MCQ question must have at least 2 options."
                                )

                except ValueError as e:
                    error_count += 1
                    failed_quizzes.add(quiz)
                    self.message_user(request, str(e), messages.ERROR)
                    continue

            # Update valid quizzes
            successful_quizzes = queryset.exclude(id__in=[q.id for q in failed_quizzes])
            success_count = successful_quizzes.count()

            if success_count:
                successful_quizzes.update(is_published=True)
                self.message_user(
                    request,
                    f"{success_count} quizzes published successfully.",
                    messages.SUCCESS
                )

            if error_count:
                self.message_user(
                    request,
                    f"{error_count} quizzes failed validation.",
                    messages.WARNING
                )

            return None  # Return to list view

        # If this is a GET request, show confirmation page
        context = {
            'quizzes': queryset,
            'title': "Confirm Quiz Publication",
            'opts': self.model._meta,
        }
        return render(request, 'admin/publish_confirmation.html', context)

    publish_quiz.short_description = "Publish selected quizzes"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'publish-confirmation/',
                self.admin_site.admin_view(self.publish_quiz),
                name='publish_quiz'
            ),
        ]
        return custom_urls + urls


admin.site.register(Quiz, QuizAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text', 'question_type',)
    search_fields = ('quiz__title', 'text',)
    list_filter = ('quiz', 'question_type',)
    ordering = ('-quiz',)


admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct', 'order',)
    search_fields = ('question__quiz__title', 'question__text', 'text',)
    list_filter = ('question__quiz', 'question', 'is_correct', 'order',)
    ordering = ('-question__quiz', '-question', 'order',)
    form = AnswerModelForm


admin.site.register(Answer, AnswerAdmin)
