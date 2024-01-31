from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message , Conversation , PrivateNotification
from core.models import User
import json
import datetime
from .tasks import send_notification_task
class ChatConsumer(AsyncWebsocketConsumer):
    typing_list =[]
    async def connect(self):

        if not( await self.get_data()):
            self.close()

        else :
            await self.channel_layer.group_add(
                self.room_id,
                self.channel_name
            )
            await self.accept()


    async def disconnect(self, close_code):
        # Leave the private chat room
        await self.channel_layer.group_send(
                self.room_id,
                {
                    'type': 'chat_message',
                    'message': None,
                    'sender': self.sender.username,
                    'receiver': self.receiver.username,
                    'time' : None,
                    'is_typing':False
                }
            )
        await self.channel_layer.group_discard(
            self.room_id,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive a message from one of the users and send it to the other user in the room
        text_data_json = json.loads(text_data)

        if 'message' in text_data_json:
            message = text_data_json['message']
            message = await self.create_message(message)
            await self.channel_layer.group_send(
                self.room_id,
                {
                    'type': 'chat_message',
                    'message': message.content,
                    'sender': self.sender.username,
                    'receiver': self.receiver.username,
                    'time' : message.time.strftime("%Y-%m-%d %H:%M:%S"),
                    'is_typing':False
                }
            )
            send_notification_task.apply_async(args=[self.sender.username,self.receiver.username])
        else :
            is_typing = text_data_json['is_typing']
            await self.channel_layer.group_send(
                self.room_id,
                {
                    'type': 'chat_message',
                    'message': None,
                    'sender': self.sender.username,
                    'receiver': self.receiver.username,
                    'time' : None,
                    'is_typing':is_typing
                }
            )


        
        
    
    async def chat_message(self, event):
        # Receive a message from the channel layer, and send it to the user who is not the sender
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        time = event['time']
        if "is_typing" in event :
            is_typing  = event['is_typing']
        else :
            is_typing=False
        if is_typing and sender not in self.typing_list :
            self.typing_list.append(sender)
        elif not is_typing and sender in self.typing_list :
            self.typing_list.remove(sender)

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
            'time': time,
            'typing_list':self.typing_list
        }))
        await self.create_notification(self.sender , self.receiver)

    @database_sync_to_async
    def create_notification(self ,from_user , to_user):
        PrivateNotification.objects.create(from_user = from_user , to_user= to_user).save()
    @database_sync_to_async
    def create_message(self,message):
        # Create a new message object and save it to the database
        return Message.objects.create(sender=self.sender, receiver=self.receiver, content=message,conversation=self.conversation)
    
    @database_sync_to_async
    def get_data(self):
        self.sender = self.scope['user']
        self.room_id = "0"
        if not self.sender.is_authenticated :
            return False
        try:
            self.receiver = User.objects.get(username =self.scope['url_route']['kwargs']['username'])
        except User.DoesNotExist:
            return False
        try :
            self.conversation = Conversation.objects.filter(user1=self.sender, user2=self.receiver).union(
            Conversation.objects.filter(user1=self.receiver, user2=self.sender))[0]
        except IndexError:
            self.conversation= Conversation.objects.create(user1=self.sender , user2= self.receiver )
        self.room_id = str(self.conversation.room_id).replace("-","_")    
        return True
    


class PrivateNotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        if not( await self.get_data()):
            self.close()
        else:
            await self.channel_layer.group_add(self.username, self.channel_name)
            await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.username, self.channel_name)
        
    async def send_notification(self, event):
        from_username = event["username"]
        await self.send(text_data=json.dumps(
            {
                "username": from_username
            }))
    
    @database_sync_to_async
    def get_data(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated :
            return False
        self.username =str(self.user.username)
        return True


