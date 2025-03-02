import django_filters  # Импортируем django_filters для создания фильтров
from django import forms  # Импортируем формы Django для настройки виджетов
from .models import Post, Category  # Импортируем модели Post и Category

# Создаём фильтр для модели Post
class PostFilter(django_filters.FilterSet):
    # Фильтр по заголовку, ищет по подстроке (регистр не учитывается)
    post_title = django_filters.CharFilter(
        lookup_expr='icontains',  # Поиск по вхождению подстроки (без учёта регистра)
        label='Заголовок'  # Подпись к полю в форме фильтрации
    )

    # Фильтр по тексту, ищет по подстроке
    post_text = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Текст'
    )

    # Фильтр по имени автора (ищет внутри связанной модели Author)
    author__full_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Автор'
    )

    # Фильтр по категории, выбирая из списка существующих категорий
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),  # Берём все существующие категории
        field_name='category',  # Поле, по которому фильтруем
        to_field_name='name',  # Используем название категории, а не ID
        label='Категория'
    )

    # Фильтр по типу поста (Статья или Новость)
    post_type = django_filters.ChoiceFilter(
        choices=Post.POST_TYPES,  # Используем предопределённые варианты
        label='Тип поста'
    )

    # Фильтр по диапазону дат с виджетами календаря
    created_at = django_filters.DateFromToRangeFilter(
        label='Дата создания',  # Подпись в форме
        widget=django_filters.widgets.RangeWidget(  # Используем специальный виджет для диапазона дат
            attrs={'type': 'date', 'class': 'form-control'}  # Указываем тип поля (календарь) и стили
        )
    )

    # Определяем, к какой модели относится фильтр и какие поля можно фильтровать
    class Meta:
        model = Post  # Используем модель Post
        fields = ['post_title', 'post_text', 'author__full_name', 'category', 'post_type', 'created_at']  # Список фильтруемых полей