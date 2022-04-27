from django.contrib import admin

from OnlineQuizPlatform.auth_app.models import Profile, QuizUser


class ProfileInLineAdmin(admin.StackedInline):
    model = Profile


@admin.register(QuizUser)
class ProfileAdmin(admin.ModelAdmin):
    inlines = (ProfileInLineAdmin,)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
