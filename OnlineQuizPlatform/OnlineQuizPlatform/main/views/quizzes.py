from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from OnlineQuizPlatform.auth_app.models import Profile
from OnlineQuizPlatform.main.forms.quizzes import CreateQuizForm, DeleteQuizForm
from OnlineQuizPlatform.main.models import Quiz, Question, QuizResult


class CreateQuizView(views.CreateView):
    template_name = 'main/quiz_create.html'
    form_class = CreateQuizForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('subcategory details', kwargs={'pk': self.object.subcategory.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs


class QuizDetailsView(views.DetailView):
    model = Quiz
    template_name = 'main/quiz_details.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        questions = Question.objects.filter(quiz_id=self.object.id)

        context['questions'] = questions

        return context


class EditQuizView(views.UpdateView):
    model = Quiz
    fields = ('title', 'duration', 'description')
    template_name = 'main/quiz_edit.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('quiz details', kwargs={'pk': self.object.id})


class DeleteQuizView(views.DeleteView):
    model = Quiz
    form_class = DeleteQuizForm
    template_name = 'main/quiz-delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('subcategory details', kwargs={'pk': self.object.subcategory.id})


def take_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)

    questions = Question.objects.filter(quiz_id=pk)
    try:
        quiz_result = QuizResult.objects.get(quiz=quiz, player=request.user)
    except:
        quiz_result = QuizResult(quiz=quiz, player=request.user)

    if request.method == 'POST':

        score = 0
        correct = 0
        incorrect = 0

        for question in questions:
            if question.answer == request.POST.get(question.description):
                score += 10
                correct += 1
            else:
                incorrect += 1

        taken_time = request.POST.get('timer')

        if score > quiz_result.score:
            quiz_result.score = score
            quiz_result.correct_answers = correct
            quiz_result.incorrect_answers = incorrect
            quiz_result.taken_time = int(taken_time)
            best_result = True
            quiz_result.save()
        elif score == quiz_result.score and int(taken_time) < quiz_result.taken_time:
            quiz_result.score = score
            quiz_result.correct_answers = correct
            quiz_result.incorrect_answers = incorrect
            quiz_result.taken_time = int(taken_time)
            best_result = True
            quiz_result.save()
        else:
            best_result = False

        context = {
            'score': score,
            'correct': correct,
            'incorrect': incorrect,
            'taken_time': taken_time,
            'best_result': best_result,
            'quiz_result': quiz_result,
            'quiz': quiz,
            'player': request.user,
        }
        return render(request, 'main/result.html', context)
    else:
        context = {
            'quiz': quiz,
            'questions': questions,
            'quiz_result': quiz_result,
        }
        return render(request, 'main/take-quiz.html', context)
