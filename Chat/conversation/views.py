from rest_framework import generics, permissions ,status
from rest_framework.views import APIView
from .models import Message , Conversation
from .serializers import ConversationSerializer ,MessageSerializer
from rest_framework.response import Response 
from core.models import User
from django.shortcuts import render , HttpResponse , redirect 
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView


class ListMessages(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request , username):
        try:
            user2= User.objects.get(username=username)
        except User.DoesNotExist :
            return Response({'detail':f'No such user have username {username}'})
        try:
            query = Conversation.objects.filter(
                user1 = user2 , user2 = request.user).union(Conversation.objects.filter(
                user2 = user2 , user1 = request.user) )[0]
        except IndexError :
            query = Conversation.objects.create(user1=request.user , user2= user2 )
        print(query)
        serializer = ConversationSerializer(query)
        # serializer.is_valid(raise_exception=False) 
        return Response(serializer.data , status=status.HTTP_200_OK)


# class MessageListCreateView(generics.ListCreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         # Set the sender of the message to the authenticated user
#         serializer.save(sender=self.request.user)

#     def get_queryset(self):
#         # Return only messages between the authenticated user and the other user in the private chat
#         room_name = self.kwargs.get('room_name')
#         other_user = self.kwargs.get('other_user')
#         return Message.objects.filter(sender=self.request.user, receiver=other_user).union(
#             Message.objects.filter(sender=other_user, receiver=self.request.user)
#         )

def room(request , username):
    if request.method =="GET":
        user = User.objects.get(username = username)
        return render(request , 'conversation/room.html' , {'username':username , 'last_seen':user.last_seen})

import pytz
from django.utils import timezone

def convert_to_utc(user_time ,user_timezone_offset ):
    # Convert user time to a timezone-aware datetime object
    user_datetime = timezone.datetime.strptime(user_time, '%Y-%m-%dT%H:%M')
    user_timezone = timezone.timedelta(minutes=int(user_timezone_offset))
    user_datetime_aware = timezone.make_aware(user_datetime, timezone.utc) + user_timezone

    # Convert user time to UTC
    utc_datetime = user_datetime_aware.astimezone(pytz.utc)

    return utc_datetime

from .tasks import send_periodic_message

@api_view(["POST"])
def send_periodic_messages(request, to_user):
    if not request.user.is_authenticated:
        return Response("error", status=status.HTTP_401_UNAUTHORIZED)
    utc_time = convert_to_utc(request.data['time'] , request.data['user_timezone_offset'])
    print(str(request.user.username) , str(to_user) )
    user = User.objects.get(username=str(request.user.username))
    send_periodic_message.apply_async(args=[str(request.user.username) , str(to_user) , request.data['messageP']],eta=utc_time)
    return Response("Success", status=status.HTTP_200_OK)

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class RetrieveMessages(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, username):
        sender =  request.user
        receiver = User.objects.get(username = username)
        try :
            conversation = Conversation.objects.filter(user1=sender, user2=receiver).union(
            Conversation.objects.filter(user1=receiver, user2=sender))[0]
        except IndexError:
            conversation= Conversation.objects.create(user1=sender , user2= receiver ).save()
        messages = conversation.messages.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

   
    