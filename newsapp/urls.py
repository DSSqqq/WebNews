from django.urls import path, include
# Импортируем созданное нами представление
from .views import (PostList,
                    PostDetail,
                    PostCreate,
                    PostUpdate,
                    PostDelete,
                    )


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
]