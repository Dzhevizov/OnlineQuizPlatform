from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from OnlineQuizPlatform.auth_app.models import Profile
from OnlineQuizPlatform.main.models import Quiz, QuizResult, Category, SubCategory

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

QUIZ_DATA = {
    'title': 'abv',
    'duration': '5',
    'subcategory_id': 1,
    'author_id': 1,
}

SUBCATEGORY_DATA = {
    'name': 'subcat',
    'picture': 'http://subcat.bg',
    'category_id': 1,
}

CATEGORY_DATA = {
    'name': 'cat',
    'picture': 'http://cat.bg',
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


# class UserRegisterTest(TestCase):
#
#     def test_register_when_all_data_is_valid(self):
#         Group.objects.create(name='Player')
#         # user = UserModel.objects.create_user(**VALID_USER_DATA)
#         profile_data = {
#             'username': 'testuser',
#             'email': 'testuser@abv.bg',
#             'password1': 'secret',
#             'password2': 'secret',
#             'first_name': 'Pesho',
#             'last_name': 'Ivanov',
#             'date_of_birth': date(2000, 1, 1),
#             'gender': 'Male',
#             'city': 'Varna',
#             'picture': 'http://abv.bg/',
#             'description': 'something',
#         }
#
#         self.client.post(reverse('register user'), data=profile_data, follow=True)
#         profile = Profile.objects.get()
#         self.assertIsNone(profile)
#         self.assertEqual(profile_data['first_name'], profile.first_name)
#         self.assertEqual(profile_data['last_name'], profile.last_name)
#         self.assertEqual(profile_data['date_of_birth'], profile.date_of_birth)
#         self.assertEqual(profile_data['gender'], profile.gender)
#         self.assertEqual(profile_data['city'], profile.city)
#         self.assertEqual(profile_data['picture'], profile.picture)
#         self.assertEqual(profile_data['description'], profile.description)
#         self.assertEqual(profile_data['user'], profile.user)


class ProfileDetailsViewTest(TestCase):

    def test_expect_correct_template(self):
        Group.objects.create(name='Player')
        user = UserModel.objects.create_user(**VALID_USER_DATA)
        profile = Profile.objects.create(**PROFILE_DATA, user=user)
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed('auth_user/profile_details.html')

    def test_when_opening_not_existing_profile(self):
        response = self.client.get(reverse('profile', kwargs={'pk': 1}))
        self.assertEqual(302, response.status_code)
        self.assertTemplateUsed('login.html')

    def test_when_no_quiz_results(self):
        Group.objects.create(name='Player')
        user = UserModel.objects.create_user(**VALID_USER_DATA)
        user2 = UserModel.objects.create_user(**INVALID_USER_DATA)
        profile = Profile.objects.create(**PROFILE_DATA, user=user)

        category = Category.objects.create(**CATEGORY_DATA)
        subcategory = SubCategory.objects.create(**SUBCATEGORY_DATA)
        quiz = Quiz.objects.create(**QUIZ_DATA)
        quiz_result = QuizResult.objects.create(quiz=quiz, player=user2)
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertListEqual([], response.context['quiz_results'])
