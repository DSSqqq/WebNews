from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = Post  # Добавляем явное указание модели
        fields = [
            'post_title',
            'post_text',
            'author',  # Исправлено: author__full_name → author
            'category',
            'post_type',
        ]

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        name = cleaned_data.get("post_title")  # Убедись, что поле называется "post_title"

        if name == description:
            raise ValidationError("Описание не должно быть идентично названию.")

        return cleaned_data

