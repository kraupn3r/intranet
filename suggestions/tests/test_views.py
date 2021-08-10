from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission, Group, User
from accounts.models import UserProfile
from suggestions.models import Post, Comment, BoardCategory


class TestPostListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        cls.test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')


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

        test_user2_userprofile = UserProfile.objects.create(
            user=cls.test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )

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





    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('suggestions:postlist'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/suggestions/')


    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('suggestions:postlist'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'suggestions/post_list.html')

    def test_view_if_context_passed(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('suggestions:postlist'))
        self.assertEquals(response.context['categories'].count(),2)

    def test_queryset(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('suggestions:postlist'))
        self.assertEquals(response.context['object_list'].count(),3)


class TestCategoryDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        cls.test_user2 = User.objects.create_user(username='testuser2', password='1ddsSRUkw+tuK')


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

        test_user2_userprofile = UserProfile.objects.create(
            user=cls.test_user2,
            name='Test User2',
            telephone='222222222',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
            )

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


    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('suggestions:category', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/suggestions/category/1/')

    def test_view_if_context_passed(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('suggestions:category', kwargs={'pk':1}))
        self.assertEquals(response.context['categories'].count(),2)

    def test_queryset_filtering(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('suggestions:category', kwargs={'pk':1}))
        self.assertEquals(response.context['object_list'].count(),2)


class Testpost_postView(TestCase):

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

        test_board_category1 = BoardCategory.objects.create(
            title='test title 1'
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

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('suggestions:postform'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/suggestions/upload/')

    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('suggestions:postform'))
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('suggestions:postform'),
        {'body':'test post body','title':'test post title','category':1})
        self.assertEquals(response.status_code,302)
        response = self.client.get(reverse('suggestions:postlist'))
        self.assertEquals(response.context['object_list'].count(),3)
        self.assertEquals(Post.objects.get(id=3).author,self.test_user1)


class Testpost_commentView(TestCase):

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

        test_board_category1 = BoardCategory.objects.create(
            title='test title 1'
        )



        test_post_1 = Post.objects.create(
            body='test body 1',
            title='test title 1',
            category=test_board_category1,
            author=cls.test_user1
        )

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('suggestions:postcomment', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/suggestions/1/comment/')

    def test_view_if_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('suggestions:postcomment', kwargs={'pk':1}))
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('suggestions:postcomment', kwargs={'pk':1}),
            {'body':'test post body','title':'test post title'})
        self.assertEquals(response.status_code,302)
        response = self.client.get(reverse('suggestions:postdetail', kwargs={'pk':1}))
        self.assertEquals(response.context['object'].comments.count(),1)
