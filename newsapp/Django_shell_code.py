'''
python manage.py shell

from newsapp.models import User
from newsapp.models import Post
from newsapp.models import PostCategory
from newsapp.models import Category
from newsapp.models import Category
from newsapp.models import Author
from newsapp.models import Comment

user1 = User.objects.get(username="Person123")
user2 = User.objects.get(username="qwert1234")

author1 = Author.objects.create(user=user1, full_name="Author 1")
author2 = Author.objects.create(user=user2, full_name="Author 2")

cat1 = Category.objects.create(category_name="Technology")
cat2 = Category.objects.create(category_name="Science")
cat3 = Category.objects.create(category_name="Sports")
cat4 = Category.objects.create(category_name="Politics")

post1 = Post.objects.create(post_type="article", post_title="Tech Trends", post_text="Latest in tech", author=author1)
post2 = Post.objects.create(post_type="article", post_title="Science Discovery", post_text="New breakthrough", author=author2)
post3 = Post.objects.create(post_type="news", post_title="Political Debate", post_text="Recent political events", author=author1)

post1.category.add(category1, category2)  # Статья с 2 категориями
post2.category.add(category2)
post3.category.add(category3)

comment1 = Comment.objects.create(post_comment=post1, user_comment=user2, text_comment="Great article!")
comment2 = Comment.objects.create(post_comment=post2, user_comment=user1, text_comment="Interesting discovery!")
comment3 = Comment.objects.create(post_comment=post3, user_comment=user2, text_comment="Important news.")
comment4 = Comment.objects.create(post_comment=post1, user_comment=user1, text_comment="Nice insights!")

post1.like()
post1.like()
post2.like()
post2.dislike()
post3.like()

comment1.like()
comment1.like()
comment2.dislike()
comment3.like()
comment4.like()

author1 = Author.objects.get(id=1)
author1.update_rating()
author2 = Author.objects.get(id=2)
author2.update_rating()

best_author = Author.objects.order_by('-rating').first()
print(f"Лучший автор: {best_author.user.username}, рейтинг: {best_author.rating}")

best_post = Post.objects.order_by('-post_rating').first()
print(f"Дата: {best_post.created_at}, Автор: {best_post.author.user.username}, Рейтинг: {best_post.post_rating}")
print(f"Заголовок: {best_post.post_title}")
print(f"Превью: {best_post.preview()}")

comments = Comment.objects.filter(post_comment=best_post)
for comment in comments:
    print(f"Дата: {comment.time_comment}, Пользователь: {comment.user_comment.username}, Рейтинг: {comment.rating_comment}")
    print(f"Текст: {comment.text_comment}")

'''