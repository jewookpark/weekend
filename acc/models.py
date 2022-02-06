from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    comment = models.TextField()
    pic = models.ImageField(upload_to="user/%y")
    age = models.IntegerField(default=0)
    
    def getpic(self):
        if self.pic:
            return self.pic.url
        return "/media/noimage.png"
# Create your models here.
