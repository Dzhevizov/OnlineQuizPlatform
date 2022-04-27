from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from OnlineQuizPlatform.common.validators import only_letters_validator

UserModel = get_user_model()


class Category(models.Model):
    NAME_MIN_LEN = 3
    NAME_MAX_LEN = 30

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
        validators=(
            MinLengthValidator(NAME_MIN_LEN),
            only_letters_validator,
        )
    )

    picture = models.URLField()

    description = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    NAME_MIN_LEN = 3
    NAME_MAX_LEN = 30

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
        validators=(
            MinLengthValidator(NAME_MIN_LEN),
        )
    )

    picture = models.URLField()

    description = models.TextField(
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Quiz(models.Model):
    TITLE_MIN_LEN = 5
    TITLE_MAX_LEN = 80

    DURATION_MIN_VALUE = 0

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
        unique=True,
        validators=(
            MinLengthValidator(TITLE_MIN_LEN),
        )
    )

    duration = models.IntegerField(
        validators=(
            MinValueValidator(DURATION_MIN_VALUE),
        )
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    DESCRIPTION_MAX_LEN = 150
    OPTIONS_MAX_LEN = 150
    ANSWER_MAX_LEN = 10

    description = models.CharField(
        max_length=DESCRIPTION_MAX_LEN,
    )

    option1 = models.CharField(
        max_length=OPTIONS_MAX_LEN,
    )

    option2 = models.CharField(
        max_length=OPTIONS_MAX_LEN,
    )

    option3 = models.CharField(
        max_length=OPTIONS_MAX_LEN,
    )

    option4 = models.CharField(
        max_length=OPTIONS_MAX_LEN,
    )

    answer = models.CharField(
        max_length=ANSWER_MAX_LEN,
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.description


class QuizResult(models.Model):
    SCORE_DEFAULT_VALUE = 0
    SCORE_MIN_VALUE = 0

    TAKEN_TIME_DEFAULT_VALUE = 0
    TAKEN_TIME_MIN_VALUE = 0

    CORRECT_ANSWERS_DEFAULT_VALUE = 0
    CORRECT_ANSWERS_MIN_VALUE = 0

    INCORRECT_ANSWERS_DEFAULT_VALUE = 0
    INCORRECT_ANSWERS_MIN_VALUE = 0

    score = models.IntegerField(
        default=SCORE_DEFAULT_VALUE,
        validators=(
            MinValueValidator(SCORE_MIN_VALUE),
        )
    )

    taken_time = models.IntegerField(
        default=TAKEN_TIME_DEFAULT_VALUE,
        validators=(
            MinValueValidator(TAKEN_TIME_MIN_VALUE),
        )
    )

    correct_answers = models.IntegerField(
        default=CORRECT_ANSWERS_DEFAULT_VALUE,
        validators=(
            MinValueValidator(CORRECT_ANSWERS_MIN_VALUE),
        )
    )

    incorrect_answers = models.IntegerField(
        default=INCORRECT_ANSWERS_DEFAULT_VALUE,
        validators=(
            MinValueValidator(INCORRECT_ANSWERS_MIN_VALUE),
        )
    )

    first_taken = models.DateTimeField(
        auto_now_add=True,
    )

    last_taken = models.DateTimeField(
        auto_now=True,
    )

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
    )

    player = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.score
