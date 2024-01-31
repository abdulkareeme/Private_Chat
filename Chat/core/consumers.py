from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async


online_users = []

class OnlineUsersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the consumer to the "online_users" group
        if not await self.get_data():
            await self.close()
        await self.channel_layer.group_add("online_users", self.channel_name)
        
        await self.accept()
        online_users.append(self.username)
        await self.channel_layer.group_send(
            "online_users",
            {
                "type":"send_online_users"
            }
        )
        
        

    async def disconnect(self, close_code):
        if self.user.username in online_users:
            online_users.remove(self.user.username)
            await self.make_offline()
            await self.channel_layer.group_send(
                "online_users",
                {
                    "type":"send_online_users"
                }
            )
        # Remove the consumer from the "online_users" group
        await self.channel_layer.group_discard("online_users", self.channel_name)

    async def receive(self, text_data):
        # Ignore incoming messages, as we only need to send updates to the client
        pass

    async def send_online_users(self,event):
        # Send the online user list as a JSON message to the client
        await self.send(text_data=json.dumps({
            'online_users': online_users
        }))

    @database_sync_to_async
    def get_data(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated :
            return False
        self.username =str(self.user.username)
        return True
    
    @database_sync_to_async
    def make_offline(self):
        import datetime
        self.user.last_seen = datetime.datetime.now()
        self.user.save()