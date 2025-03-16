from django_apscheduler.jobstores import DjangoJobStore, register_events
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Category
from django.contrib.auth.models import User


def send_weekly_newsletter():
    """Функция отправки писем подписчикам с новыми статьями за неделю"""
    one_week_ago = now() - timedelta(days=7)

    categories = Category.objects.all()
    for category in categories:
        # Получаем пользователей, подписанных на категорию
        subscribers = category.subscribers.all()

        if subscribers.exists():
            # Получаем новые статьи за неделю
            new_posts = Post.objects.filter(category=category, created_at__gte=one_week_ago)

            if new_posts.exists():
                # Формируем список ссылок на статьи
                post_links = "\n".join(
                    [f"- {post.post_title}: http://127.0.0.1:8000/news/{post.id}" for post in new_posts])

                # Формируем текст письма
                subject = f"Новые статьи в категории '{category.name}'"
                message = f"Здравствуйте!\n\nВот новые статьи в категории '{category.name}' за последнюю неделю:\n\n{post_links}\n\nС уважением, команда News Portal."

                # Отправляем письма подписчикам
                for user in subscribers:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def start_scheduler():
    """Настройка планировщика задач"""
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Запуск каждую неделю по воскресеньям в 9 утра
    scheduler.add_job(send_weekly_newsletter, "cron", day_of_week="sun", hour=20, minute=25, id="weekly_newsletter",
                      replace_existing=True)

    register_events(scheduler)
    scheduler.start()