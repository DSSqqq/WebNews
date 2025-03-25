from celery import shared_task
from django.utils.timezone import now, timedelta
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import Post, Category
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import json
from django.core.mail import get_connection

@shared_task
def send_weekly_newsletter():
    print("Задача send_weekly_newsletter запущена")
    """Асинхронная рассылка подписчикам с новыми статьями за неделю через Celery"""
    one_week_ago = now() - timedelta(days=7)

    messages = []
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()

        if subscribers.exists():
            new_posts = Post.objects.filter(category=category, created_at__gte=one_week_ago)

            if new_posts.exists():
                post_links = "\n".join(
                    [f"- {post.post_title}: https://127.0.0.1:8000.com/news/{post.id}" for post in new_posts]
                )

                subject = f"Новые статьи в категории '{category.name}'"
                message = f"Здравствуйте!\n\nВот новые статьи в категории '{category.name}' за последнюю неделю:\n\n{post_links}\n\nС уважением, команда News Portal."

                for user in subscribers:
                    messages.append((subject, message, settings.DEFAULT_FROM_EMAIL, [user.email]))

    if messages:
        connection = get_connection()
        connection.open()
        send_mass_mail(messages, connection=connection)
        connection.close()

def setup_periodic_tasks():
    """Настройка периодических задач в Celery Beat (еженедельная рассылка)"""
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute="0",
        hour="8",
        day_of_month="*",
        month_of_year="*",
        day_of_week="1",  # Понедельник
        timezone="UTC"
    )

    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name="Send weekly newsletter",
        task="newsapp.tasks.send_weekly_newsletter",
        defaults={"args": json.dumps([]), "enabled": True}
    )






@shared_task
def send_post_notification(post_id):
    from .models import Post  # Импорт тут, чтобы избежать циклического импорта

    post = Post.objects.get(id=post_id)
    subscribers = post.category.subscribers.all()

    if subscribers.exists():
        subject = f"Новый пост в категории '{post.category.name}'"
        message = f"Здравствуйте!\n\nОпубликован новый пост:\n\n- {post.post_title}: https://127.0.0.1:8000.com/news/{post.id}\n\nС уважением, команда News Portal."

        messages = [(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email]) for user in subscribers]

        send_mass_mail(messages)