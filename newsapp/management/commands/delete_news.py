from django.core.management.base import BaseCommand
from ...models import Post, Category
from django.core.management import CommandError


class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории после подтверждения'

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str, help='Имя категории, из которой нужно удалить все новости')

    def handle(self, *args, **kwargs):
        category_name = kwargs['category_name']

        # Проверяем, существует ли категория
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise CommandError(f'Категория "{category_name}" не найдена.')

        # Запрашиваем подтверждение
        confirmation = input(f'Вы уверены, что хотите удалить все новости из категории "{category_name}"? (y/n): ')

        if confirmation.lower() != 'y':
            self.stdout.write(self.style.WARNING('Операция отменена. Новости не удалены.'))
            return

        # Удаляем все новости из этой категории
        posts_to_delete = Post.objects.filter(category=category)
        posts_count = posts_to_delete.count()

        if posts_count == 0:
            self.stdout.write(self.style.SUCCESS(f'Нет новостей в категории "{category_name}".'))
        else:
            posts_to_delete.delete()
            self.stdout.write(self.style.SUCCESS(f'Удалено {posts_count} новостей из категории "{category_name}".'))