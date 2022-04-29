from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from OnlineQuizPlatform.main.forms.categories import CreateCategoryForm, DeleteCategoryForm
from OnlineQuizPlatform.main.models import Category, SubCategory


class CreateCategoryView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'main/category_create.html'
    form_class = CreateCategoryForm
    success_url = reverse_lazy('categories')
    permission_required = 'main.add_category'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)


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


class EditCategoryView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = Category
    fields = ('name', 'picture', 'description')
    template_name = 'main/category_edit.html'
    permission_required = 'main.change_category'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('category details', kwargs={'pk': self.object.id})


class DeleteCategoryView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = Category
    form_class = DeleteCategoryForm
    template_name = 'main/category-delete.html'
    success_url = reverse_lazy('categories')
    permission_required = 'main.delete_category'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)
