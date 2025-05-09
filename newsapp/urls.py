from django.urls import path, include
from django.views.decorators.cache import cache_page
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, PostCreate, PostUpdate, PostDelete, category_list, subscribe, unsubscribe,
                    test_log_view)


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='post_list'),  # список новостей
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),  # страница статьи

   path('create/', PostCreate.as_view(), name='post_create'),
   path('post/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/', category_list, name='category_list'),
   path('subscribe/<int:category_id>/', subscribe, name='subscribe'),
   path('unsubscribe/<int:category_id>/', unsubscribe, name='unsubscribe'),
   path('test-log/', test_log_view),
]