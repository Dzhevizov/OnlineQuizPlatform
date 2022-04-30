from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()

VALID_USER_DATA = {
    'username': 'testuser',
    'email': 'testuser@abv.bg',
    'password': 'secret'
}
INVALID_USER_DATA = {
    'username': 'testuser2',
    'email': 'testuser2@abv.bg',
    'password': 'secret'
}

PROFILE_DATA = {
    'first_name': 'Pesho',
    'last_name': 'Ivanov',
    'date_of_birth': date(2000, 1, 1),
    'gender': 'Male',
    'city': 'Varna',
    'picture': 'http://abv.bg/',
    'description': 'something',
}

PROFILE_DATA2 = {
    'username': 'testuser',
    'email': 'testuser@abv.bg',
    'first_name': 'Gosho',
    'last_name': 'Toshev',
    'date_of_birth': date(2000, 1, 1),
    'gender': 'Male',
    'city': 'Varna',
    'picture': 'http://abv.bg/',
    'description': 'something',
}


class UserLoginTest(TestCase):

    def test_login__with_valid_user_credentials(self):
        Group.objects.create(name='Player')
        UserModel.objects.create_user(**VALID_USER_DATA)
        response = self.client.post(reverse('login user'), VALID_USER_DATA, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'index.html')

    def test_login__with_invalid_user_credentials(self):
        Group.objects.create(name='Player')
        UserModel.objects.create_user(**VALID_USER_DATA)
        response = self.client.post(reverse('login user'), INVALID_USER_DATA, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'auth_user/login.html')


class UserLogoutTest(TestCase):

    def test_logout(self):
        Group.objects.create(name='Player')
        UserModel.objects.create_user(**VALID_USER_DATA)
        self.client.login(**VALID_USER_DATA)
        response = self.client.post(reverse('logout user'), VALID_USER_DATA, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'index.html')


class RestrictedViewTest(TestCase):

    def test_restricted__with_valid_user_credentials(self):
        Group.objects.create(name='Player')
        UserModel.objects.create_user(**VALID_USER_DATA)
        response = self.client.post(reverse('restricted'), VALID_USER_DATA, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'index.html')

    def test_restricted__with_invalid_user_credentials(self):
        Group.objects.create(name='Player')
        UserModel.objects.create_user(**VALID_USER_DATA)
        response = self.client.post(reverse('restricted'), INVALID_USER_DATA, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'auth_user/403.html')
