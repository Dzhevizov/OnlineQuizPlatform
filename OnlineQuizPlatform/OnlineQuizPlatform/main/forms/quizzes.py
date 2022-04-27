from django import forms

from OnlineQuizPlatform.common.helpers import BootstrapFormMixin
from OnlineQuizPlatform.main.models import Quiz


class CreateQuizForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, author, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.author = author
        self._init_bootstrap_form_control()

    def save(self, commit=True):
        quiz = super().save(commit=False)

        quiz.author = self.author
        if commit:
            quiz.save()

        return quiz

    class Meta:
        model = Quiz
        fields = ('title', 'duration', 'description', 'subcategory')


class DeleteQuizForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Quiz
        fields = ()
