from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    ChoiceSerializer, PollSerializer, VoteSerializer)
from rest_framework.response import Response
from rest_framework import status
from .models import Choice, Poll
from django.shortcuts import get_object_or_404


class PollViewSet(ModelViewSet):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ChoiceListAPI(generics.ListCreateAPIView):
    """Получить список сущностей или создать их. Позволяет GET и POST"""

    #queryset = Choice.objects.all()
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset

    serializer_class = ChoiceSerializer



class CreateVoteAPI(APIView):
    serializer_class = VoteSerializer

    def post(self, request, pk, choice_pk):
        vote_by = request.data.get('vote_by')
        data = {'choice': choice_pk, 'poll': pk, 'vote_by': vote_by}
        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)