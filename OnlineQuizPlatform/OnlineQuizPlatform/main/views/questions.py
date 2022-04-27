from django.urls import reverse_lazy
from django.views import generic as views

from OnlineQuizPlatform.main.forms.questions import CreateQuestionForm, DeleteQuestionForm
from OnlineQuizPlatform.main.models import Question


class CreateQuestionView(views.CreateView):
    template_name = 'main/question_create.html'
    form_class = CreateQuestionForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('quiz details', kwargs={'pk': self.object.quiz.id})


class EditQuestionView(views.UpdateView):
    model = Question
    fields = ('description', 'option1', 'option2', 'option3', 'option4', 'answer')
    template_name = 'main/question_edit.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('quiz details', kwargs={'pk': self.object.quiz.id})


class DeleteQuestionView(views.DeleteView):
    model = Question
    form_class = DeleteQuestionForm
    template_name = 'main/question-delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('quiz details', kwargs={'pk': self.object.quiz.id})
