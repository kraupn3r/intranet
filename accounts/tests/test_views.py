from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Permission


class TestEmployeelistView(TestCase):

    @classmethod
    def setUpTestData(cls):

        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user3 = User.objects.create_user(
            username='testuser3', password='2HJ1vRVkw+3iD')
        test_user4 = User.objects.create_user(
            username='testuser4', password='2Hkw+RV0Z&3iD')

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
        )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='22',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
        )

        test_user3_userprofile = UserProfile.objects.create(
            user=test_user3,
            name='Test User3',
            telephone='33',
            email='testuser3@email.com',
            employee_id='4',
            departament='mar',
            location='KRK',
        )

        test_user4_userprofile = UserProfile.objects.create(
            user=test_user4,
            name='Test User4',
            telephone='33',
            email='testuser4@email.com',
            employee_id='5',
            departament='HR',
            location='KRK'
        )

        test_user1_userprofile.save()
        test_user2_userprofile.save()
        test_user3_userprofile.save()
        test_user4_userprofile.save()

        cls.list_url = 'accounts:employees'

    def test_EmployeeListView_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(self.list_url))
        self.assertRedirects(
            response, '/accounts/login/?next=/accounts/employees/')

    def test_EmployeeListView_GET_logged_in(self):

        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse(self.list_url))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'accounts/userprofile_list.html')

    def test_EmployeeListView_queryset(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse(self.list_url))
        self.assertEquals(response.context['object_list'].count(), 4)
        response = self.client.get(reverse('accounts:employees') + '?q=3')
        self.assertEquals(response.context['object_list'].count(), 2)


class TestUserProfileDetailView(TestCase):

    @classmethod
    def setUpTestData(cls):

        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
        )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='22',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
        )

        test_user1_userprofile.save()
        test_user2_userprofile.save()

    def test_UserProfileDetailView_if_not_logged_in(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertRedirects(
            response, '/accounts/login/?next=/accounts/profile')

    def test_UserProfileDetailView_logged_in(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'accounts/userprofile_detail.html')


class TestEditProfileView(TestCase):

    @classmethod
    def setUpTestData(cls):

        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
        )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='22',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
        )

        test_user1_userprofile.save()
        test_user2_userprofile.save()

    def test_edit_profile_not_logged_in(self):
        response = self.client.get(reverse('accounts:edit_profile'))
        self.assertRedirects(
            response, '/accounts/login/?next=/accounts/profile/edit')

    def test_edit_profile_if_logged_in(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('accounts:edit_profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/editprofile.html')


class TestRegisterView(TestCase):

    @classmethod
    def setUpTestData(cls):

        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            departament='HR',
            location='WAW'
        )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='22',
            email='testuser2@email.com',
            departament='sal',
            location='PZN'
        )

        test_user1_userprofile.save()
        test_user2_userprofile.save()
        permission = Permission.objects.get(name='Can add user')
        test_user2.user_permissions.add(permission)

        test_user2.save()

    def test_views_not_logged_in(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertRedirects(
            response, '/accounts/login/?next=/accounts/register/')

    def test_views_if_logged_in_no_permission(self):
        login = self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('accounts:register'))
        self.assertEquals(response.status_code, 403)

    def test_views_if_logged_in_has_permission(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('accounts:register'))
        self.assertEquals(response.status_code, 200)

    def test_register(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        data = {
            'name': 'test_name3',
            'telephone': '1212',
            'username': 'test_user3',
            'email': 'test_email@email.com',
            'location': 'non',
            'departament': 'non',
            'position': 'trainee'
        }
        response = self.client.post(reverse('accounts:register'), data=data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(UserProfile.objects.get(id=3).name, 'test_name3')
        self.assertEquals(UserProfile.objects.get(id=3).employee_id, 4)
        self.assertEquals(
            len(UserProfile.objects.get(id=3).first_login_string), 30)
        self.assertEquals(UserProfile.objects.get(id=3).is_active, False)
        self.assertEquals(UserProfile.objects.get(id=3).user,
                          User.objects.get(username='test_user3'))
        self.assertEquals(UserProfile.objects.get(id=3).email,
                          User.objects.get(username='test_user3').email)


class TestFirstLoginView(TestCase):

    @classmethod
    def setUpTestData(cls):

        test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')

        cls.test_user1_userprofile = UserProfile.objects.create(
            user=test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            departament='HR',
            location='WAW',
            is_active=True
        )

        test_user2_userprofile = UserProfile.objects.create(
            user=test_user2,
            name='Test User2',
            telephone='22',
            email='testuser2@email.com',
            departament='sal',
            location='PZN'
        )

        permission = Permission.objects.get(name='Can add user')
        test_user2.user_permissions.add(permission)

        test_user2.save()

    def test_views_if_account_active(self):
        response = self.client.get(reverse('accounts:first_login', kwargs={
                                   'string': self.test_user1_userprofile.first_login_string}))
        self.assertEquals(response.status_code, 403)

    def test_views_if_redirects_when_account_not_active(self):
        login = self.client.login(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        data = {
            'name': 'test_name3',
            'telephone': '1212',
            'username': 'test_user3',
            'email': 'test_email@email.com',
            'location': 'non',
            'departament': 'non',
            'position': 'trainee'
        }
        response = self.client.post(reverse('accounts:register'), data=data)
        response = self.client.get(reverse('accounts:first_login', kwargs={
                                   'string': UserProfile.objects.get(id=3).first_login_string}))
        self.assertEquals(response.status_code, 302)
