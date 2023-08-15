from django.db import models

# Create your models here.


class Conversions(models.Model):
    participants = models.ManyToManyField(
        'auth.User', related_name='conversations')


class Message(models.Model):
    conversion = models.ForeignKey(
        Conversions, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
