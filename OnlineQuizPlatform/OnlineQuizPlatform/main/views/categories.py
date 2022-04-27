from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import generic as views

from OnlineQuizPlatform.main.forms.categories import CreateCategoryForm, DeleteCategoryForm
from OnlineQuizPlatform.main.models import Category, SubCategory


class CreateCategoryView(views.CreateView):
    template_name = 'main/category_create.html'
    form_class = CreateCategoryForm

    success_url = reverse_lazy('categories')




class CategoriesView(views.ListView):
    model = Category
    template_name = 'main/categories.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all().order_by('name')

        context['categories'] = categories

        return context


class CategoryDetailsView(views.DetailView):
    model = Category
    template_name = 'main/category_details.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subcategories = SubCategory.objects.filter(category_id=self.object.id).order_by('name')

        context['subcategories'] = subcategories

        return context


class EditCategoryView(views.UpdateView):
    model = Category
    fields = ('name', 'picture', 'description')
    template_name = 'main/category_edit.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('category details', kwargs={'pk': self.object.id})


class DeleteCategoryView(views.DeleteView):
    model = Category
    form_class = DeleteCategoryForm
    template_name = 'main/category-delete.html'

    success_url = reverse_lazy('categories')
