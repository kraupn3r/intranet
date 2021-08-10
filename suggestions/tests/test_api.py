import json
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from rest_framework.test import APIRequestFactory, APITestCase
from ..models import Post, BoardCategory, Comment
from ..api.views import PostListAPIView, CommentAPIView, PostDetailAPIView, BoardCategoryListAPIView
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


class TestPostListAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

        newgroup = Group.objects.create(name='testgroup')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)

        test_user1_userprofile = UserProfile.objects.create(
            user=cls.test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='sal',
            location='WAW'
        )
        test_user1_userprofile.save()

        cls.factory = APIRequestFactory()

        test_board_category1 = BoardCategory.objects.create(
            title='test title 1'
        )

        test_board_category2 = BoardCategory.objects.create(
            title='test title 2'
        )

        test_post_1 = Post.objects.create(
            body='test body 1',
            title='test title 1',
            category=test_board_category1,
            author=cls.test_user1
        )
        test_post_2 = Post.objects.create(
            body='test body 2',
            title='test title 2',
            category=test_board_category1,
            author=cls.test_user1
        )
        test_post_3 = Post.objects.create(
            body='test body 3',
            title='test title 3',
            category=test_board_category2,
            author=cls.test_user1
        )
        test_comment1 = Comment.objects.create(
            Post=test_post_1,
            body='test comment body 1',
            author=cls.test_user1
        )
        test_comment2 = Comment.objects.create(
            Post=test_post_2,
            body='test comment body 2',
            author=cls.test_user1
        )

    def test_queryset(self):
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/suggestions/api/postlist/',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = PostListAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(len(json.loads(response.content)), 3)

    def test_queryset_w_params(self):
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/suggestions/api/postlist/?id=2',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = PostListAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(len(json.loads(response.content)), 1)

    def test_post_create(self):
        user = self.test_user1
        token = get_token(user)
        data = {
            'body': 'test body 4',
            'title': 'test title 4',
            'category': '1'
        }
        request = self.factory.post(
            '/suggestions/api/postlist/', data,
            HTTP_AUTHORIZATION='JWT ' + token)
        view = PostListAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(response.status_code, 201)

        request = self.factory.get(
            '/suggestions/api/postlist/',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = PostListAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(len(json.loads(response.content)), 4)


class TestPostDetailAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

        newgroup = Group.objects.create(name='testgroup')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)

        test_user1_userprofile = UserProfile.objects.create(
            user=cls.test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='sal',
            location='WAW'
        )
        test_user1_userprofile.save()

        cls.factory = APIRequestFactory()

        test_board_category1 = BoardCategory.objects.create(
            title='test title 1'
        )

        test_board_category2 = BoardCategory.objects.create(
            title='test title 2'
        )

        test_post_1 = Post.objects.create(
            body='test body 1',
            title='test title 1',
            category=test_board_category1,
            author=cls.test_user1
        )
        test_post_2 = Post.objects.create(
            body='test body 2',
            title='test title 2',
            category=test_board_category1,
            author=cls.test_user1
        )
        test_post_3 = Post.objects.create(
            body='test body 3',
            title='test title 3',
            category=test_board_category2,
            author=cls.test_user1
        )
        test_comment1 = Comment.objects.create(
            Post=test_post_1,
            body='test comment body 1',
            author=cls.test_user1
        )
        test_comment2 = Comment.objects.create(
            Post=test_post_2,
            body='test comment body 2',
            author=cls.test_user1
        )
        # print(json.loads(response.content))

    def test_queryset(self):
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/suggestions/api/1',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = PostDetailAPIView.as_view()
        response = view(request, pk=1)
        response.render()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(json.loads(response.content)), 8)


class TestCommentAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

        newgroup = Group.objects.create(name='testgroup')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)

        test_user1_userprofile = UserProfile.objects.create(
            user=cls.test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='sal',
            location='WAW'
        )
        test_user1_userprofile.save()

        cls.factory = APIRequestFactory()

        test_board_category1 = BoardCategory.objects.create(
            title='test title 1'
        )

        test_post_1 = Post.objects.create(
            body='test body 1',
            title='test title 1',
            category=test_board_category1,
            author=cls.test_user1
        )

    def test_comment_create(self):
        user = self.test_user1
        token = get_token(user)
        data = {
            'Post': 1,
            'body': 'test comment body',

        }
        request = self.factory.post(
            '/suggestions/api/comment/', data,
            HTTP_AUTHORIZATION='JWT ' + token)
        view = CommentAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(response.status_code, 201)
        expected_response = {'Post': 1, 'body': 'test comment body'}
        self.assertEquals(json.loads(response.content), expected_response)
        request = self.factory.get(
            '/suggestions/api/1',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = PostDetailAPIView.as_view()
        response = view(request, pk=1)
        response.render()

        self.assertEquals(len(json.loads(response.content)['comments']), 1)


class TestBoardCategoryListAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

        newgroup = Group.objects.create(name='testgroup')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)

        test_user1_userprofile = UserProfile.objects.create(
            user=cls.test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='sal',
            location='WAW'
        )
        test_user1_userprofile.save()

        cls.factory = APIRequestFactory()

        test_board_category1 = BoardCategory.objects.create(
            title='test title 1'
        )

        test_board_category2 = BoardCategory.objects.create(
            title='test title 2'
        )

    def test_queryset(self):
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/suggestions/api/',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = BoardCategoryListAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(len(json.loads(response.content)), 2)
