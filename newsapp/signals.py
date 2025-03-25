from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import send_post_notification
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Проверяем, новый ли пользователь
        print(f"Создан новый пользователь: {instance.email}")
        subject = "Добро пожаловать в News Portal!"
        message = (
            f"Здравствуйте, {instance.username}!\n\n"
            "Спасибо за регистрацию в нашем новостном портале.\n"
            "Теперь вы можете подписываться на категории, комментировать статьи и получать свежие новости прямо на почту.\n\n"
            "С уважением, команда News Portal."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])


@receiver(post_save, sender=Post)
def send_notification_on_post_save(sender, instance, created, **kwargs):
    if created:  # Если пост только что создан
        send_post_notification.delay(instance.id)