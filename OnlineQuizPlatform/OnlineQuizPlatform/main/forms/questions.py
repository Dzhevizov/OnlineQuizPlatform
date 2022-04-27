from django import forms

from OnlineQuizPlatform.common.helpers import BootstrapFormMixin
from OnlineQuizPlatform.main.models import Question


class CreateQuestionForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_control()

    class Meta:
        model = Question
        fields = ('description', 'option1', 'option2', 'option3', 'option4', 'answer', 'quiz')


class DeleteQuestionForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Question
        fields = ()
