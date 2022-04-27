from django.contrib import admin

from OnlineQuizPlatform.main.models import Category, SubCategory, Quiz, Question


class SubCategoryInLineAdmin(admin.StackedInline):
    model = SubCategory


class QuizInLineAdmin(admin.StackedInline):
    model = Quiz


class QuestionInLineAdmin(admin.StackedInline):
    model = Question


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (SubCategoryInLineAdmin,)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    inlines = (QuizInLineAdmin,)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = (QuestionInLineAdmin,)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
