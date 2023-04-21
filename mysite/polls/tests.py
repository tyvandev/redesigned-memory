import datetime

from django.core.exceptions import ValidationError

from django.test import TestCase

from django.urls import reverse

from django.utils import timezone
from django.utils import timezone

from .models import Question, Choice

QUESTION_TEXT = 'Demo question text'
VIEWNAME = 'polls:detail'

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTest(TestCase):

	def test_question_text_uniqueness(self):
		create_question(QUESTION_TEXT, 0)
		with self.assertRaises(ValidationError) as raised:
		    question = create_question(QUESTION_TEXT, 0)
		    question.validate_constraints()
		self.assertEqual(ValidationError, type(raised.exception))

    def test_was_published_recently_with_current_question(self):
	    time = timezone.now()
	    future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), True)

	def test_was_published_recently_with_past_question(self):
		time = timezone.now() + datetime.timedelta(days=-30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)

		self.assertIs(future_question.was_published_recently(), False)


def create_choice(question, choice_text, votes=0):
    return Choice.objects.create(
		question=question,
		choice_text=choice_text,
		votes=votes)


class ChoiceModelTest(TestCase):

	def setUp(self):
		self.choice_text = 'True'
		self.question = create_question(QUESTION_TEXT, 0)

		create_choice(self.question, self.choice_text)

	def test_choice_question_uniqueness(self):
		with self.assertRaises(ValidationError) as raised:
			choice = create_choice(self.question, self.choice_text)
			choice.validate_constraints()
		self.assertEqual(ValidationError, type(raised.exception))


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_current_question(self):
        question = create_question(QUESTION_TEXT, 0)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )


class QuestionDetailViewTests(TestCase):
    def test_non_existent_question(self):
        url = reverse(VIEWNAME, args=(12,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_current_question(self):
        question = create_question(QUESTION_TEXT, 0)
        url = reverse(VIEWNAME, args=(question.id,))
        response = self.client.get(url)

        self.assertContains(response, question.question_text)

    def test_current_question_with_choice(self):
        question = create_question(QUESTION_TEXT, 0)
        choice1 = create_choice(question, 'true')
        choice2 = create_choice(question, 'false')
        url = reverse(VIEWNAME, args=(question.id,))
        response = self.client.get(url)

        self.assertContains(response, question.question_text)
        self.assertContains(response, choice1.choice_text)
        self.assertContains(response, choice2.choice_text)