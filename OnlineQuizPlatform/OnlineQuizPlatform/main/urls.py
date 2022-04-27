from django.urls import path

from OnlineQuizPlatform.main.views.categories import CreateCategoryView, CategoriesView, CategoryDetailsView, \
    EditCategoryView, DeleteCategoryView
from OnlineQuizPlatform.main.views.questions import CreateQuestionView, EditQuestionView, DeleteQuestionView
from OnlineQuizPlatform.main.views.quizzes import CreateQuizView, QuizDetailsView, EditQuizView, DeleteQuizView, \
    take_quiz
from OnlineQuizPlatform.main.views.subcategories import CreateSubCategoryView, SubCategoryDetailsView, \
    EditSubCategoryView, DeleteSubCategoryView

urlpatterns = (
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('categories/create/', CreateCategoryView.as_view(), name='create category'),
    path('categories/details/<int:pk>/', CategoryDetailsView.as_view(), name='category details'),
    path('categories/edit/<int:pk>/', EditCategoryView.as_view(), name='edit category'),
    path('categories/delete/<int:pk>/', DeleteCategoryView.as_view(), name='delete category'),

    path('subcategories/create/', CreateSubCategoryView.as_view(), name='create subcategory'),
    path('subcategories/details/<int:pk>/', SubCategoryDetailsView.as_view(), name='subcategory details'),
    path('subcategories/edit/<int:pk>/', EditSubCategoryView.as_view(), name='edit subcategory'),
    path('subcategories/delete/<int:pk>/', DeleteSubCategoryView.as_view(), name='delete subcategory'),

    path('quizzes/create/', CreateQuizView.as_view(), name='create quiz'),
    path('quizzes/details/<int:pk>/', QuizDetailsView.as_view(), name='quiz details'),
    path('quizzes/edit/<int:pk>/', EditQuizView.as_view(), name='edit quiz'),
    path('quizzes/delete/<int:pk>/', DeleteQuizView.as_view(), name='delete quiz'),
    path('quizzes/take/<int:pk>/', take_quiz, name='take quiz'),

    path('questions/create/', CreateQuestionView.as_view(), name='create question'),
    path('questions/edit/<int:pk>/', EditQuestionView.as_view(), name='edit question'),
    path('questions/delete/<int:pk>/', DeleteQuestionView.as_view(), name='delete question'),

)
