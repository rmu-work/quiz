from django import forms

from .models import Quiz
from .models import Answer


class QuizModelForm(forms.ModelForm):
    def clean_time_limit(self):
        time_limit = self.cleaned_data.get('time_limit')
        if time_limit < 1:
            raise forms.ValidationError("Time limit must be at least 1 minute.")
        return time_limit

    class Meta:
        model = Quiz
        fields = '__all__'


class AnswerModelForm(forms.ModelForm):

    def clean(self):
        question = self.cleaned_data.get('question')
        order = self.cleaned_data.get('order')

        if question.question_type != 'MCQ' and question.answers.all().count() > 0:
            raise forms.ValidationError("Only MCQ questions can have multiple options.")

        if question.question_type != 'MCQ':
            is_correct = self.cleaned_data.get('is_correct')
            if not is_correct:
                raise forms.ValidationError("Besides MCQ questions all other need to mark is_correct flag.")

        if not self.instance:
            if Answer.objects.filter(question=question, order=order).exists():
                raise forms.ValidationError("Answer with this order already exists for this question.")
        else:
            if Answer.objects.filter(question=question, order=order, id__ne=self.instance.id).exists():
                raise forms.ValidationError("Answer with this order already exists for this question.")

    class Meta:
        model = Answer
        fields = '__all__'
