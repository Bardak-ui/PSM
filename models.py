from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='send_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.recipient}: {self.content}'

class DataUser(models.Model):
    profile_name = models.CharField(max_length=50, verbose_name="Псевдоним")
    age = models.PositiveIntegerField(verbose_name="Возраст")
    status = models.CharField(max_length=100, verbose_name="Статус")
    
    def __str__(self):
        return self.profile_name