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
}

SUBCATEGORY_DATA = {
    'name': 'subcat',
    'picture': 'http://subcat.bg',
}

CATEGORY_DATA = {
    'name': 'cat',
    'picture': 'http://cat.bg',
}


class ProfileDetailsViewTest(TestCase):

    def test_expect_correct_template(self):
        Group.objects.create(name='Player')
        user = UserModel.objects.create_user(**VALID_USER_DATA)
        profile = Profile.objects.create(**PROFILE_DATA, user=user)
        self.client.login(**VALID_USER_DATA)
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
        self.client.login(**VALID_USER_DATA)
        category = Category.objects.create(**CATEGORY_DATA)
        subcategory = SubCategory.objects.create(category=category, **SUBCATEGORY_DATA)
        quiz = Quiz.objects.create(subcategory=subcategory, author=user2, **QUIZ_DATA)
        quiz_result = QuizResult.objects.create(quiz=quiz, player=user2)
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}), follow=True)
        self.assertListEqual([], list(response.context.get('quiz_results')))
        self.assertEqual(0, response.context.get('taken_quizzes_count'))
        self.assertEqual(0, response.context.get('average_result'))
        self.assertEqual('newbie', response.context.get('rank'))


    def test_with_quiz_results(self):
        Group.objects.create(name='Player')
        user = UserModel.objects.create_user(**VALID_USER_DATA)
        user2 = UserModel.objects.create_user(**INVALID_USER_DATA)
        profile = Profile.objects.create(**PROFILE_DATA, user=user)
        self.client.login(**VALID_USER_DATA)
        category = Category.objects.create(**CATEGORY_DATA)
        subcategory = SubCategory.objects.create(category=category, **SUBCATEGORY_DATA)
        quiz = Quiz.objects.create(subcategory=subcategory, author=user2, **QUIZ_DATA)
        quiz_result = QuizResult.objects.create(quiz=quiz, player=user)
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}), follow=True)
        self.assertListEqual([quiz_result], list(response.context.get('quiz_results')))
        self.assertEqual(1, response.context.get('taken_quizzes_count'))
        self.assertEqual(0, response.context.get('average_result'))
        self.assertEqual('newbie', response.context.get('rank'))


class ShowQuizResultsViewTest(TestCase):

    def test_expect_correct_template(self):
        Group.objects.create(name='Player')
        user = UserModel.objects.create_user(**VALID_USER_DATA)
        profile = Profile.objects.create(**PROFILE_DATA, user=user)
        self.client.login(**VALID_USER_DATA)
        response = self.client.get(reverse('quiz results', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed('auth_user/quiz_results.html')

    def test_with_quiz_results(self):
        Group.objects.create(name='Player')
        user = UserModel.objects.create_user(**VALID_USER_DATA)
        user2 = UserModel.objects.create_user(**INVALID_USER_DATA)
        profile = Profile.objects.create(**PROFILE_DATA, user=user)
        self.client.login(**VALID_USER_DATA)
        category = Category.objects.create(**CATEGORY_DATA)
        subcategory = SubCategory.objects.create(category=category, **SUBCATEGORY_DATA)
        quiz = Quiz.objects.create(subcategory=subcategory, author=user2, **QUIZ_DATA)
        quiz_result = QuizResult.objects.create(quiz=quiz, player=user)
        response = self.client.get(reverse('quiz results', kwargs={'pk': profile.pk}), follow=True)
        self.assertListEqual([quiz_result], list(response.context.get('quiz_results')))


class ShowCreatedQuizzesViewTest(TestCase):

    def test_expect_correct_template(self):
        Group.objects.create(name='Player')
        user = UserModel.objects.create_user(**VALID_USER_DATA)
        profile = Profile.objects.create(**PROFILE_DATA, user=user)
        self.client.login(**VALID_USER_DATA)
        response = self.client.get(reverse('created quizzes', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed('auth_user/created_quizzes.html')

    def test_with_quiz_results(self):
        Group.objects.create(name='Player')
        user = UserModel.objects.create_user(**VALID_USER_DATA)
        user2 = UserModel.objects.create_user(**INVALID_USER_DATA)
        profile = Profile.objects.create(**PROFILE_DATA, user=user)
        self.client.login(**VALID_USER_DATA)
        category = Category.objects.create(**CATEGORY_DATA)
        subcategory = SubCategory.objects.create(category=category, **SUBCATEGORY_DATA)
        quiz = Quiz.objects.create(subcategory=subcategory, author=user, **QUIZ_DATA)
        response = self.client.get(reverse('created quizzes', kwargs={'pk': profile.pk}), follow=True)
        self.assertListEqual([quiz], list(response.context.get('created_quizzes')))
