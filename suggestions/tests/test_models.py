from django.test import TestCase
from accounts.models import UserProfile
from django.contrib.auth.models import User
from suggestions.models import BoardCategory, Post, Comment


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

        test_user1_userprofile = UserProfile.objects.create(
            user=cls.test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
        )

        test_board_category1 = BoardCategory.objects.create(
            title='test title 1'
        )

        cls.test_post = Post.objects.create(
            body='test body',
            author=cls.test_user1,
            title='test title',
            category=test_board_category1
        )

    def test_post_title_label(self):
        field_label = self.test_post._meta.get_field(
            'title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_post_body_label(self):
        field_label = self.test_post._meta.get_field(
            'body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_post_author_label(self):
        field_label = self.test_post._meta.get_field(
            'author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_post_title_max_length(self):
        max_length = self.test_post._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_post_body_max_length(self):
        max_length = self.test_post._meta.get_field('body').max_length
        self.assertEqual(max_length, 500)

    def test_post_object_name(self):
        expected_object_name = self.test_post.title
        self.assertEqual(str(self.test_post), expected_object_name)

    def test_post_absolute_url(self):
        expected_url = '/suggestions/1/'
        self.assertEqual(self.test_post.get_absolute_url(), expected_url)


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

        test_user1_userprofile = UserProfile.objects.create(
            user=cls.test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
        )

        test_board_category1 = BoardCategory.objects.create(
            title='test title 1'
        )

        cls.test_post = Post.objects.create(
            body='test body',
            author=cls.test_user1,
            title='test title',
            category=test_board_category1
        )
        cls.test_comment = Comment.objects.create(
            body='test body',
            author=cls.test_user1,
            Post=cls.test_post
        )

    def test_comment_body_label(self):
        field_label = self.test_comment._meta.get_field(
            'body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_comment_author_label(self):
        field_label = self.test_comment._meta.get_field(
            'author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_comment_body_max_length(self):
        max_length = self.test_comment._meta.get_field('body').max_length
        self.assertEqual(max_length, 500)

    def test_comment_object_name(self):
        expected_object_name = self.test_comment.body[:20]
        self.assertEqual(str(self.test_comment), expected_object_name)
