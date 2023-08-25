from django.db import models
from PIL import Image
import os
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        # show how we want it to be displayed
        return f'{self.user.username} Profile'

    @property
    def full_name(self):
        full_name = self.user.first_name+self.user.last_name
        return full_name if len(full_name) > 0 else self.user.username

    def remvove_old_image(self):
        cur_obj = Profile.objects.filter(id=self.id).first()
        if cur_obj and 'media\default.png' not in cur_obj.image.path:
            file_path = cur_obj.image.path
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print("PATH NOT EXIST")

    def save(self):
        self.remvove_old_image()
        super().save()
        img = Image.open(self.image.path)
        if img.height > 96 or img.width > 96:
            output_size = (96, 96)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        db_table = "profile"


class Conversions(models.Model):
    roomId = ShortUUIDField()
    participants = models.ManyToManyField(
        'auth.User', related_name='conversations')

    def __str__(self):
        return self.roomId

    class Meta:
        db_table = "conversions"


class Message(models.Model):
    conversion = models.ForeignKey(
        Conversions, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = "messages"
