from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from django.db.utils import IntegrityError
from django.core.exceptions import FieldError
from datetime import date
import uuid

from polls.models import Poll, Question, Choice
from polls.serializers import PollSerializer, QuestionSerializer, ChoiceSerializer


class PollViewSet(viewsets.ModelViewSet):
    '''
    Handels Polls views
    '''
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def get_queryset(self):
        queryset = Poll.objects.all()
        if self.request.user.is_superuser:
            return queryset
        else:
            today = date.today()
            queryset = queryset.filter(expire_date__gte=today)
            return queryset

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            poll = data.pop('poll')
            poll, created = Poll.objects.update_or_create(**poll)
            poll.save()
            if created:
                return Response('Created poll id: %d' % poll.id, status=status.HTTP_201_CREATED)
            else:
                return Response('Updated poll id: %d' % poll.id, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except FieldError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class QuestionViewSet(viewsets.ModelViewSet):
    '''
    Handels Questions views
    '''

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', ]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Creates new question in poll for admin POST request
        # Creates answer model for user POST request
        # not explicit but does the job
        data = request.data
        try:
            if self.request.user.is_superuser:  # checking if user is admin
                question = data.pop('question')
                poll = Poll.objects.get(pk=int(self.kwargs['poll_pk']))
                # creating or updating poll question
                question, created = Question.objects.update_or_create(
                                                            poll=poll,
                                                            question_type=question['question_type'],
                                                            question_text=question['question_text'],
                )
                question.save()
                if created:
                    return Response('Created question id: %d' % question.id, status=status.HTTP_201_CREATED)
                else:
                    return Response('Updated question id: %d' % question.id, status=status.HTTP_200_OK)
            else:  # if user is not admin
                answers = data.pop('answers')
                for answer in answers:
                    poll = Poll.objects.get(pk=int(self.kwargs['poll_pk']))
                    try:
                        question = Question.objects.get(pk=int(answer['question_id']))
                    except Question.DoesNotExist:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    # creating choice model for every answers
                    choice = Choice.objects.create(
                                                poll=poll,
                                                question=question,
                                                user_id=answer['user_id'],
                                                choice_text=answer['choice_text'],
                    )
                    choice.save()
                return Response('Answers are accepted', status=status.HTTP_201_CREATED)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except FieldError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChoiceViewSet(viewsets.ModelViewSet):
    '''
    Handels Choices views
    '''

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.all()
        if self.request.user.is_superuser:
            return queryset
        else:
            u_id = self.request.query_params.get('uid', None)
            if u_id is not None:
                queryset = queryset.filter(user_id=u_id.title())
            return queryset


class KeyGen(viewsets.ViewSet):
    def list(self, request, pk=None):
        uid = uuid.uuid4()
        return Response('Your new id: %s' % uid, status=status.HTTP_201_CREATED)
