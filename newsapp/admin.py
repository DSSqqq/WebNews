from django.contrib import admin
from .models import Category, Post, Author, Comment

class PostAdmin(admin.ModelAdmin):
    # Только нужные поля, а не всё подряд. Это красиво и удобно.
    list_display = ('post_title', 'post_type', 'author', 'category', 'created_at', 'post_rating')
    # Фильтровать по авторам, типу поста и категории
    list_filter = ('post_type', 'category', 'author', 'created_at')
    # Искать по заголовку, тексту поста и юзернейму автора.
    # author__user__username — потому что Author ссылается на User, и имя юзера живёт в user.username.
    search_fields = ('post_title', 'post_text', 'author__user__username')
    # позволяет быстро прыгать по датам создания.
    date_hierarchy = 'created_at'
    # Сортирует по дате, самые новые — сверху
    ordering = ['-created_at']

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comment)