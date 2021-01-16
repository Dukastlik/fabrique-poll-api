from django.db import models
from datetime import datetime


class Poll(models.Model):
    title = models.CharField(max_length=127, unique=True)
    pub_date = models.DateTimeField('date published', editable=False)
    expire_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


class Question(models.Model):
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=127)
    question_text = models.CharField(max_length=255)

    class Meta:
        unique_together = ('poll', 'question_text')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='poll', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    user_id = models.UUIDField(editable=False)
    choice_text = models.CharField(max_length=255)

    class Meta:
        unique_together = ('poll', 'question', 'user_id')

    def __str__(self):
        return self.choice_text
