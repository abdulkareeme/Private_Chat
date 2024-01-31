from django.db import models
from django.contrib.auth.models import AbstractUser
from knox.models import AuthToken

class User(AbstractUser):
    last_seen = models.DateTimeField(auto_now=True)
    


class ChatKey(AuthToken):
    pass
