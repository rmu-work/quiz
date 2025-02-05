from django.contrib import admin

from .models import Category
from .models import Quiz
from .models import Question
from .models import Answer


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)
    ordering = ('name',)


admin.site.register(Category, CategoryAdmin)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'created_by',)
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


admin.site.register(Answer, AnswerAdmin)
