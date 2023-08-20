from django.db import models
from PIL import Image
import os
from django.conf import settings
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        # show how we want it to be displayed
        return f'{self.user.username} Profile'

    def remvove_old_image(self):
        cur_obj = Profile.objects.filter(id=self.id).first()
        if cur_obj:
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


class Conversions(models.Model):
    participants = models.ManyToManyField(
        'auth.User', related_name='conversations')

    def __str__(self) -> str:
        obj_name = ''
        if len(self.participants.all()) == 2:
            obj_name = self.participants.all(
            )[0].username+" & "+self.participants.all()[1].username
        else:
            for user in self.participants.all():
                obj_name += user.username+','
        return obj_name


class Message(models.Model):
    conversion = models.ForeignKey(
        Conversions, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
