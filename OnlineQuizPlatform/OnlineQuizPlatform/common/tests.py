from datetime import date
from unittest import TestCase

from django.core.exceptions import ValidationError

from OnlineQuizPlatform.common.validators import only_letters_validator, MinDateValidator


class OnlyLettersValidatorTest(TestCase):
    correct_value = 'pesho'
    incorrect_value = 'pesho2'

    def test_when_value_is_correct(self):
        self.assertEqual(None, only_letters_validator(self.correct_value))

    def test_when_value_contains_digit(self):
        with self.assertRaises(ValidationError) as ex:
            only_letters_validator(self.incorrect_value)

        self.assertIsNotNone(ex.exception)


class MinDateValidatorTest(TestCase):
    correct_date = date(2000, 5, 10)
    incorrect_date = date(1900, 2, 6)

    def test_when_date_is_valid(self):
        date_validator = MinDateValidator(date(1920, 1, 1))
        self.assertEqual(None, date_validator(self.correct_date))

    def test_when_date_is_invalid(self):
        date_validator = MinDateValidator(date(1920, 1, 1))
        with self.assertRaises(ValidationError) as ex:
            date_validator(self.incorrect_date)

        self.assertIsNotNone(ex.exception)
