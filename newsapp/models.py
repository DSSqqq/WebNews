from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг всех статей автора, умноженный на 3
        post_ratings = sum(post.post_rating * 3 for post in Post.objects.filter(author=self))

        # Суммарный рейтинг всех комментариев автора
        comment_ratings = sum(comment.rating_comment for comment in Comment.objects.filter(user_comment=self.user))

        # Суммарный рейтинг всех комментариев к статьям автора
        post_comment_ratings = sum(
            comment.rating_comment for comment in Comment.objects.filter(post_comment__author=self))

        # Обновление рейтинга автора
        self.rating = post_ratings + comment_ratings + post_comment_ratings
        self.save()

# Категория, к которой будет привязываться Новость
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Подписчики категории (ManyToMany с User)
    subscribers = models.ManyToManyField(User, related_name="subscribed_categories", blank=True)

    def __str__(self):
        return self.name.title()

class Post(models.Model):

    ARTICLE = "article"
    NEWS = "news"

    POST_TYPES = [
        (ARTICLE, "Статья"),
        (NEWS, "Новость"),
    ]
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default=NEWS) #Выбор статья или новость вефолт новость
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    post_title = models.CharField(max_length=255) #заголовок
    post_text = models.TextField() # текст новости
    post_rating = models.IntegerField(default=0)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)  # Связь один ко многим с моделью автор
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news', # все продукты в категории будут доступны через поле news
    )

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Проверяем, создаётся ли пост впервые
        super().save(*args, **kwargs)
        if is_new:
            self.notify_subscribers()

    def notify_subscribers(self):
        subscribers = self.category.subscribers.all()
        emails = [user.email for user in subscribers if user.email]

        if emails:
            send_mail(
                subject=f"Новая статья в категории {self.category.name}",
                message=f"Прочитайте новую статью: {self.post_title}\n{self.preview()}\n\nЧитать полностью: http://127.0.0.1:8000{self.get_absolute_url()}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=False,
            )
    def __str__(self):
        return f'{self.post_title}: {self.post_text[:20]}'

    def like(self):
        self.post_rating +=1
        self.save()

    def dislike(self):
        self.post_rating -=1
        self.save()

    def preview(self):
        return self.post_text[:124] + "..." if len(self.post_text) > 124 else self.post_text

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey("Post",on_delete=models.CASCADE) #Один ко многим с пост
    category = models.ForeignKey("Category", on_delete=models.CASCADE) #Один ко многим с категорией

class Comment(models.Model):
    post_comment = models.ForeignKey("Post", on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment +=1
        self.save()

    def dislike(self):
        self.rating_comment -=1
        self.save()

