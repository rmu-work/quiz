from django import forms

from .models import Category
from .models import Quiz
from .models import Question
from.models import Answer


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class QuizModelForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = (
            'created_by',
            'created_at',
        )


class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerModelForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'

