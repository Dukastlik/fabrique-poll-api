from polls.models import Poll, Question, Choice
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'question_type', 'question_text',)


class PollSerializer(serializers.ModelSerializer):

    questions = serializers.StringRelatedField(many=True, allow_empty=True)

    class Meta:
        model = Poll
        fields = ('id',
                  'title',
                  'pub_date',
                  'expire_date',
                  'questions',
                  )


class ChoiceSerializer(serializers.ModelSerializer):

    poll = serializers.StringRelatedField()
    question = serializers.StringRelatedField()

    class Meta:
        model = Choice
        fields = ('poll', 'question', 'choice_text',)
