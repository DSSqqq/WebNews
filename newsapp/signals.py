from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

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
