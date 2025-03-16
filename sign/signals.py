from django.db.models.signals import post_save
from django.contrib.auth.models import Group, User
from django.dispatch import receiver

@receiver(post_save, sender=User)
def add_to_default_group(sender, instance, created, **kwargs):
    if created:  # Если пользователь только что создан
        group, _ = Group.objects.get_or_create(name='common')  # Группа по умолчанию
        instance.groups.add(group)