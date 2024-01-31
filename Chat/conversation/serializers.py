from rest_framework import serializers
from .models import Message ,Conversation

class MessageSerializer(serializers.ModelSerializer):
    class Meta :
        model = Message
        fields = ['sender' , 'receiver' , 'time' , 'content']
        
class ConversationSerializer (serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    class Meta :
        model = Conversation 
        fields = ['room_name', 'messages']

# class MessageSerializer(serializers.ModelSerializer):
#     sender = serializers.ReadOnlyField(source='sender.username')
#     receiver = serializers.ReadOnlyField(source='receiver.username')

#     class Meta:
#         model = Message
#         fields = ['sender', 'receiver', 'content', 'timestamp']