from django.conf import settings
import shutil
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework.test import APIRequestFactory, APITestCase
from ..api.views import *
from django.test import override_settings
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


MEDIA_ROOT = tempfile.mkdtemp()


def get_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


class TestsUserProfileListAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')
        cls.test_user2 = User.objects.create_user(
            username='testuser2', password='2HJ1vRV0Z&3iD')
        cls.test_user3 = User.objects.create_user(
            username='testuser3', password='2HJ1vRVkw+3iD')
        cls.test_user4 = User.objects.create_user(
            username='testuser4', password='2Hkw+RV0Z&3iD')

        test_user1_userprofile = UserProfile.objects.create(
            user=cls.test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
        )

        test_user2_userprofile = UserProfile.objects.create(
            user=cls.test_user2,
            name='Test User2',
            telephone='22',
            email='testuser2@email.com',
            employee_id='3',
            departament='sal',
            location='PZN'
        )

        test_user3_userprofile = UserProfile.objects.create(
            user=cls.test_user3,
            name='Test User3',
            telephone='33',
            email='testuser3@email.com',
            employee_id='4',
            departament='mar',
            location='KRK',
        )

        test_user4_userprofile = UserProfile.objects.create(
            user=cls.test_user4,
            name='Test User4',
            telephone='33',
            email='testuser4@email.com',
            employee_id='5',
            departament='HR',
            location='KRK'
        )

        newgroup = Group.objects.create(name='testgroup')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)
        cls.factory = APIRequestFactory()

    def test_queryset_no_params(self):
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/accounts/api/list/',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = UserProfileListAPIView.as_view()

        response = view(request)
        response.render()
        # print(json.loads(response.content))
        self.assertEquals(len(json.loads(response.content)), 4)

    def test_queryset_w_params(self):
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/accounts/api/list/?q=3',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = UserProfileListAPIView.as_view()

        response = view(request)
        response.render()
        self.assertEquals(len(json.loads(response.content)), 2)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestUserProfileDetailAPIView(APITestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

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

        newgroup = Group.objects.create(name='testgroup')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)
        cls.factory = APIRequestFactory()

        test_image_path = 'accounts/tests/test_image/dino.jpg'
        cls.test_image = open(test_image_path, 'rb')
        cls.simple_file_image = SimpleUploadedFile(name="testimage.jpg",  content=open(
            test_image_path, 'rb').read(), content_type='image/jpeg')

    def test_get_response(self):
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/accounts/api/profile/',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = UserProfileDetailAPIView.as_view()

        response = view(request)
        response.render()
        expected_respone = {'profile_pic': 'http://testserver/media/profile_pics/default-profile.png', 'name': 'Test User1',
                            'telephone': 11, 'email': 'testuser1@email.com', 'position': 'trainee', 'departament': 'HR', 'location': 'WAW'}
        self.assertEquals(json.loads(response.content), expected_respone)

    def test_change_profile_picture(self):
        user = self.test_user1
        token = get_token(user)
        files = {
            'file': self.simple_file_image
        }
        request = self.factory.patch(
            '/accounts/api/profile/', data=files, HTTP_AUTHORIZATION='JWT ' + token)
        view = UserProfileDetailAPIView.as_view()

        response = view(request)
        response.render()
        expected_respone = 'Profile picture has been changed'
        user.refresh_from_db()
        expected_image = "testimage.jpg"
        self.assertEquals(self.test_user1.userprofile.profile_pic.path.split(
            '\\')[-1:][0], expected_image)
        self.assertEquals(json.loads(response.content), expected_respone)
        request = self.factory.patch(
            '/accounts/api/profile/', HTTP_AUTHORIZATION='JWT ' + token)
        view = UserProfileDetailAPIView.as_view()

        response = view(request)
        response.render()
        expected_respone = 'Profile picture has been set to default'
        self.assertEquals(json.loads(response.content), expected_respone)


class TestUserChangePasswordAPIView(APITestCase):

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

        newgroup = Group.objects.create(name='testgroup')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)
        cls.factory = APIRequestFactory()

    def test_wrong_current_pw(self):
        user = self.test_user1
        token = get_token(user)
        data = {
            'current_password': 'wrongpassword',
            'new_password': 'newpass',
            'new_password2': 'newpass'
        }
        request = self.factory.put(
            '/accounts/api/change_pw/', data,
            HTTP_AUTHORIZATION='JWT ' + token)
        view = UserChangePasswordAPIView.as_view()

        response = view(request)
        response.render()
        expected_respone = {'current_password': ['Wrong password.']}

        self.assertEquals(json.loads(response.content), expected_respone)

    def test_different_new_pws(self):
        user = self.test_user1
        token = get_token(user)
        data = {
            'current_password': '1X<ISRUkw+tuK',
            'new_password': 'newpass',
            'new_password2': 'newpass2'
        }
        request = self.factory.put(
            '/accounts/api/change_pw/', data,
            HTTP_AUTHORIZATION='JWT ' + token)
        view = UserChangePasswordAPIView.as_view()

        response = view(request)
        response.render()
        expected_respone = {'non_field_errors': ['Passwords must match']}

        self.assertEquals(json.loads(response.content), expected_respone)

    def test_change_password(self):
        user = self.test_user1
        token = get_token(user)
        data = {
            'current_password': '1X<ISRUkw+tuK',
            'new_password': 'newpass',
            'new_password2': 'newpass'
        }
        request = self.factory.put(
            '/accounts/api/change_pw/', data,
            HTTP_AUTHORIZATION='JWT ' + token)
        view = UserChangePasswordAPIView.as_view()

        response = view(request)
        response.render()
        expected_respone = 'Password has been changed'
        # print(json.loads(response.content))
        self.assertEquals(json.loads(response.content), expected_respone)


class TestAuthAPIView(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK', email='testuser1@email.com')

        test_user1_userprofile = UserProfile.objects.create(
            user=cls.test_user1,
            name='Test User1',
            telephone='11',
            email='testuser1@email.com',
            employee_id='2',
            departament='HR',
            location='WAW'
        )

        newgroup = Group.objects.create(name='testgroup')
        for each in Permission.objects.all():
            newgroup.permissions.add(each)

        cls.test_user1.groups.add(newgroup)
        cls.factory = APIRequestFactory()

    def test_get_token(self):

        data = {
            'username': 'testuser1',
            'password': '1X<ISRUkw+tuK',

        }
        request = self.factory.post(
            '/accounts/api', data)
        view = AuthAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(response.status_code, 200)
        token = response.data['token']
        request = self.factory.get(
            '/accounts/api/profile/',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = UserProfileDetailAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(response.status_code, 200)

    def test_get_token_w_email(self):

        data = {
            'username': 'testuser1@email.com',
            'password': '1X<ISRUkw+tuK',

        }
        request = self.factory.post(
            '/accounts/api', data)
        view = AuthAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(response.status_code, 200)
        token = response.data['token']
        request = self.factory.get(
            '/accounts/api/profile/',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = UserProfileDetailAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(response.status_code, 200)

    def test_wrong_credentials(self):

        data = {
            'username': 'testuser1',
            'password': 'wrongpassword',

        }
        request = self.factory.post(
            '/accounts/api', data)
        view = AuthAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEquals(response.status_code, 401)
        expected_respone = {'detail': 'Invalid credentials'}

        self.assertEquals(json.loads(response.content), expected_respone)
