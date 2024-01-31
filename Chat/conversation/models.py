from django.db import models
from core.models import User
import uuid
# Create your models here.

class Conversation(models.Model)    :
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    room_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return 'Conversation between '+str(self.user1)+' and '+str(self.user2)
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)

    class Meta : 
        ordering = ["-time"]
    def __str__(self):
        return self.content+' '+str(self.time)

class PrivateNotification(models.Model):
    from_user = models.ForeignKey("core.User", on_delete=models.CASCADE , related_name="from_user")
    to_user = models.ForeignKey("core.User", on_delete=models.CASCADE , related_name="to_user")

    def __str__(self) -> str:
        return "notification form "+str(self.from_user.username)+" to "+str(self.to_user.username)
