from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Group, Post, Comment, Follow

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Группа для теста',
        )
        cls.post = Post.objects.create(author=cls.user,
                                       text='Тестовый текст',
                                       )
        cls.comment = Comment.objects.create(author=cls.user,
                                             post=cls.post,
                                             text='Тестовый комментарий')

    def test_models_have_correct_object_name(self):
        """Проверяем, что у модели корректно работает метод __str__."""
        post = PostModelTest.post
        group = PostModelTest.group
        comment = PostModelTest.comment
        expected_values = {
            post.text[:15]: str(post)[:15],
            group.title: str(group),
            comment.text[:15]: str(comment)[:15]
        }
        for field, expected_value in expected_values.items():
            with self.subTest(field=field):
                self.assertEqual(field, expected_value)

    def test_model_have_correct_verbose_name(self):
        """Проверяем, что у модели корректные verbose_name"""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'created': 'Дата создания',
            'author': 'Автор',
            'group': 'Группа',
            'image': 'Картинка',

        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_models_have_correct_help_texts(self):
        """Проверяем, что у модели корректные help_text."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
