# Generated by Django 4.2.4 on 2023-08-17 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]
