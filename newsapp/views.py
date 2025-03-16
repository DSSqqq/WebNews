from django.shortcuts import (
    render, get_object_or_404, redirect
)

from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin
)

from django.urls import reverse_lazy

from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView,
)

from .filters import PostFilter

from .forms import (
    PostForm

)
from .models import (
    Post,Category,
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10 # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        #С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному посту
    model = Post
    # Используем другой шаблон
    template_name = 'post_detail.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'post'


# Добавляем новое представление для создания .
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def test_func(self):
        return self.request.user.groups.filter(name="authors").exists()

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def test_func(self):
        return self.request.user.groups.filter(name="authors").exists()

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.request.user.groups.filter(name="authors").exists()


# Отображение списка категорий
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'news/category_list.html', {'categories': categories})

# Подписка на категорию
@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect('category_list')

# Отписка от категории
@login_required
def unsubscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.remove(request.user)
    return redirect('category_list')