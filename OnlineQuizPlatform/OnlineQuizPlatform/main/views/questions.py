from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from OnlineQuizPlatform.main.forms.questions import CreateQuestionForm, DeleteQuestionForm
from OnlineQuizPlatform.main.models import Question


class CreateQuestionView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'main/question_create.html'
    form_class = CreateQuestionForm
    permission_required = 'main.add_question'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('quiz details', kwargs={'pk': self.object.quiz.id})


class EditQuestionView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = Question
    fields = ('description', 'option1', 'option2', 'option3', 'option4', 'answer')
    template_name = 'main/question_edit.html'
    permission_required = 'main.change_question'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('quiz details', kwargs={'pk': self.object.quiz.id})


class DeleteQuestionView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = Question
    form_class = DeleteQuestionForm
    template_name = 'main/question-delete.html'
    permission_required = 'main.delete_question'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('quiz details', kwargs={'pk': self.object.quiz.id})
