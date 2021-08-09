import json
from django.urls import reverse
from accounts.models import UserProfile
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework.test import APIRequestFactory, APITestCase
from ..models import Day, Devent
from ..api.views import DeventDetailAPIView, CalendarAPIView
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_token(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token




class TestCalendarAPIView(APITestCase):

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

        start_date = date(2020, 1, 1)
        end_date = date(2020, 2, 1)
        delta = timedelta(days=1)
        while start_date <= end_date:
            Day.objects.create(date=start_date)
            start_date += delta


        test_devent = Devent.objects.create(
                        day=Day.objects.get(date=date(2020,1,2)),
                        title='test devent',
                        author=cls.test_user1,
                        description='trr',
                        start = '00:00',
                        end = '12:00')

        test_devent2 = Devent.objects.create(
                        day=Day.objects.get(date=date(2020,1,20)),
                        title='test devent',
                        author=cls.test_user1,
                        description='trr',
                        start = '00:00',
                        end = '12:00')

    def test_queryset_both_params(self):
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/calendary/api/?min_date=2020-01-01&max_date=2020-01-31',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = CalendarAPIView.as_view()

        response = view(request)
        response.render()
        self.assertEquals(len(json.loads(response.content)), 2)

    def test_queryset_one_param(self):
        user = self.test_user1
        token = get_token(user)
        request = self.factory.get(
            '/calendary/api/?min_date=2020-01-02',
            HTTP_AUTHORIZATION='JWT ' + token)
        view = CalendarAPIView.as_view()

        response = view(request)
        response.render()
        self.assertEquals(len(json.loads(response.content)), 1)

    def test_post_devent(self):
        user = self.test_user1
        token = get_token(user)
        data = {
             'day':'2020-01-20',
             'title':'test devent post',
             'description':'test description'
        }
        request = self.factory.post(
            '/calendar/api/',data,HTTP_AUTHORIZATION='JWT ' + token, format='json')
        view = CalendarAPIView.as_view()
        response = view(request)
        response.render()

        expected_respone = {'id': 3, 'day': '2020-01-20', 'title': 'test devent post', 'description': 'test description', 'start': '00:00', 'end': '23:59'}
        self.assertEquals(json.loads(response.content), expected_respone)



class TestDeventAPIView(APITestCase):

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
            telephone='111111111',
            email='testuser1@email.com',
            employee_id='2',
            departament='sal',
            location='WAW'
        )
        test_user1_userprofile.save()

        cls.factory = APIRequestFactory()

        start_date = date(2020, 1, 1)
        end_date = date(2020, 2, 1)
        delta = timedelta(days=1)
        while start_date <= end_date:
            Day.objects.create(date=start_date)
            start_date += delta

        test_devent = Devent.objects.create(
                        day=Day.objects.get(date=date(2020,1,2)),
                        title='test devent',
                        author=cls.test_user1,
                        description='test description',
                        )


    def test_get(self):
        user = self.test_user1
        token = get_token(user)

        request = self.factory.get(
            '/calendar/api/devent/1/',HTTP_AUTHORIZATION='JWT ' + token, format='json')
        view = DeventDetailAPIView.as_view()
        response = view(request, pk = 1)
        response.render()
        expected_respone = {'id': 1, 'day': '2020-01-02', 'title': 'test devent', 'description': 'test description', 'start': '00:00:00', 'end': '23:59:00'}
        self.assertEquals(json.loads(response.content), expected_respone)

    def test_patch_gets_pk(self):
        user = self.test_user1
        token = get_token(user)
        data = {
             'day':'2020-01-20',
             'title':'test devent patch',
             'description':'test description'
        }
        request = self.factory.patch(
            '/calendar/api/devent/1/',data,HTTP_AUTHORIZATION='JWT ' + token, format='json')
        view = DeventDetailAPIView.as_view()
        response = view(request, pk = 1)
        response.render()
        expected_respone = {'id': 1, 'day': '2020-01-20', 'title': 'test devent patch', 'description': 'test description', 'start': '00:00:00', 'end': '23:59:00'}
        self.assertEquals(json.loads(response.content), expected_respone)

    def test_delete(self):
        user = self.test_user1
        token = get_token(user)

        request = self.factory.delete(
            '/calendar/api/devent/1/',HTTP_AUTHORIZATION='JWT ' + token, format='json')
        view = DeventDetailAPIView.as_view()
        response = view(request, pk = 1)
        request = self.factory.get(
            '/calendar/api/devent/1/',HTTP_AUTHORIZATION='JWT ' + token, format='json')
        view = DeventDetailAPIView.as_view()
        response = view(request, pk = 1)
        response.render()

        expected_respone = {'detail': 'Not found.'}
        self.assertEquals(json.loads(response.content), expected_respone)
