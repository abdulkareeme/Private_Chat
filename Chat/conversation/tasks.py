from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import PrivateNotification
from core.models import User
from conversation.models import Conversation , Message

@shared_task
def send_notification_task(from_user, to_user ):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(to_user),
        {
            "type": "send_notification",
            "username": from_user
        }
    )

def get_room_id(sender ,receiver ):
        room_id = "0"
        try :
            conversation = Conversation.objects.filter(user1=sender, user2=receiver).union(
            Conversation.objects.filter(user1=receiver, user2=sender))[0]
        except IndexError:
            conversation= Conversation.objects.create(user1=sender , user2= receiver )
        room_id = str(conversation.room_id).replace("-","_")    
        return (room_id,conversation)


@shared_task
def send_periodic_message(from_user, to_user, message):
    from_user = User.objects.get(username=from_user)
    to_user = User.objects.get(username=to_user)
    room_id, conversation = get_room_id(from_user, to_user)
    my_message = Message.objects.create(sender=from_user, receiver=to_user, content=message, conversation=conversation)
    my_message.save()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_id,
         {
            'type': 'chat_message',
            'message': my_message.content,
            'sender': from_user.username,
            'receiver': to_user.username,
            'time' : my_message.time.strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(to_user.username),
        {
            "type": "send_notification",
            "username": from_user.username
        }
    )

