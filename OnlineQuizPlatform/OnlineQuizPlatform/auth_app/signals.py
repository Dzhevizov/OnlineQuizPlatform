from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from OnlineQuizPlatform.auth_app.models import QuizUser


@receiver(post_save, sender=QuizUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='Player'))
