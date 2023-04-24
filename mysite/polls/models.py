import datetime

from django.db import models

from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('question_text').desc(),
                name='question_text_unique',
                violation_error_message='Question text must be unique'
            )
        ]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('choice_text').desc(),
                'question',
                name='question_choice_text_unique',
                violation_error_message='Choice text must be unique for a question'
            )
        ]