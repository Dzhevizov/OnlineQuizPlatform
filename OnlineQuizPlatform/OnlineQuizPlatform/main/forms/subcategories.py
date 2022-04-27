from django import forms

from OnlineQuizPlatform.common.helpers import BootstrapFormMixin
from OnlineQuizPlatform.main.models import SubCategory


class CreateSubCategoryForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_control()

    class Meta:
        model = SubCategory
        fields = ('name', 'picture', 'description', 'category')


class DeleteSubCategoryForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = SubCategory
        fields = ()
