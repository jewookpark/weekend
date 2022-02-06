from django.db import models
from acc.models import User

# Create your models here.
class Board(models.Model):
    subject = models.CharField(max_length=200)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    content = models.TextField()
    likey = models.ManyToManyField(User, blank=True, related_name="likey")
    pubdate = models.DateTimeField()

    def __str__(self):
        return f"{self.writer}_{self.subject}"

    def summary(self):
        if len(self.content) > 30:
            return self.content[:30] + " ..."
        return self.content
    
class Reply(models.Model):
    b = models.ForeignKey(Board, on_delete=models.CASCADE)
    replyer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    pubdate = models.DateTimeField()

    def __str__(self):
        return f"{self.b}({self.replyer})"