from django.shortcuts import render
from rest_framework import generics
from rest_framework import views
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    ChoiceSerializer, PollSerializer, VoteSerializer, UserSerializer)
from rest_framework.response import Response
from rest_framework import status
from .models import Choice, Poll
from rest_framework import permissions
from django.contrib.auth import authenticate

class PollViewSet(ModelViewSet):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, BasicAuthentication)

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pl\k'])
        if not request.user == poll.created_by:
            raise PermissionError('Вы не можете удалить этот опрос')
        return super().destroy(request, *args, **kwargs)


class ChoiceListAPI(generics.ListCreateAPIView):
    """Получить список сущностей, или создать их. Позволяет GET и POST"""

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset

    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionError('Вы не можете опубликовать вариант ответа')
        return super().post(request, *args, **kwargs)




class CreateVoteAPI(views.APIView):
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


class UserCreateAPI(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class LoginViewAPI(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
