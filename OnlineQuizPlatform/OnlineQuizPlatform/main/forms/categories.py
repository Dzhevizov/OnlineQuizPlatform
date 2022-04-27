from django import forms

from OnlineQuizPlatform.common.helpers import BootstrapFormMixin
from OnlineQuizPlatform.main.models import Category


class CreateCategoryForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_control()

    class Meta:
        model = Category
        fields = ('name', 'picture', 'description')


class DeleteCategoryForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Category
        fields = ()
