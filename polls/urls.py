from django.urls import path, include
from rest_framework import routers
from .views import (
    PollViewSet, ChoiceListAPI, CreateVoteAPI, UserCreateAPI, LoginViewAPI)

app_name = 'poll_api'

router = routers.DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')


urlpatterns = [
    #path('polls/', PollListAPI.as_view(), name='poll_list'),
    #path('poll/<int:pk>/', PollDetailAPI.as_view(), name='poll_detail'),
    path('', include(router.urls)),
    path('choices/', ChoiceListAPI.as_view(), name='choices'),
    path('polls/<int:pk>/choices/<int:choice_pk>/vote/', CreateVoteAPI.as_view(), name='create_vote'),
    path('users/', UserCreateAPI.as_view(), name='user_create'),
    path('login/', LoginViewAPI.as_view(), name='login'),

]
