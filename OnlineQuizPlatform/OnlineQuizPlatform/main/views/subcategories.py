from django.urls import reverse_lazy
from django.views import generic as views

from OnlineQuizPlatform.main.forms.subcategories import CreateSubCategoryForm, DeleteSubCategoryForm
from OnlineQuizPlatform.main.models import SubCategory, Quiz, QuizResult


class CreateSubCategoryView(views.CreateView):
    template_name = 'main/subcategory_create.html'
    form_class = CreateSubCategoryForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('category details', kwargs={'pk': self.object.category.id})


class SubCategoryDetailsView(views.DetailView):
    model = SubCategory
    template_name = 'main/subcategory_details.html'
    context_object_name = 'subcategory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        quizzes = Quiz.objects.filter(subcategory_id=self.object.id).order_by('-created_on')

        context['quizzes'] = quizzes

        return context


class EditSubCategoryView(views.UpdateView):
    model = SubCategory
    fields = ('name', 'picture', 'description')
    template_name = 'main/subcategory_edit.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('subcategory details', kwargs={'pk': self.object.id})


class DeleteSubCategoryView(views.DeleteView):
    model = SubCategory
    form_class = DeleteSubCategoryForm
    template_name = 'main/subcategory-delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('category details', kwargs={'pk': self.object.category.id})
