from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from OnlineQuizPlatform.main.forms.subcategories import CreateSubCategoryForm, DeleteSubCategoryForm
from OnlineQuizPlatform.main.models import SubCategory, Quiz


class CreateSubCategoryView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    template_name = 'main/subcategory_create.html'
    form_class = CreateSubCategoryForm
    permission_required = 'main.add_subcategory'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)

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


class EditSubCategoryView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = SubCategory
    fields = ('name', 'picture', 'description')
    template_name = 'main/subcategory_edit.html'
    permission_required = 'main.change_subcategory'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('subcategory details', kwargs={'pk': self.object.id})


class DeleteSubCategoryView(auth_mixins.LoginRequiredMixin, auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = SubCategory
    form_class = DeleteSubCategoryForm
    template_name = 'main/subcategory-delete.html'
    permission_required = 'main.delete_subcategory'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('restricted')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('category details', kwargs={'pk': self.object.category.id})
