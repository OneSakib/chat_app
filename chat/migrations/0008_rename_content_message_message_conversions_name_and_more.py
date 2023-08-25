# Generated by Django 4.2.4 on 2023-08-24 02:34

from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_conversions_table_alter_message_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='content',
            new_name='message',
        ),
        migrations.AddField(
            model_name='conversions',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='conversions',
            name='roomId',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, length=22, max_length=22, prefix=''),
        ),
        migrations.AddField(
            model_name='conversions',
            name='type',
            field=models.CharField(default='DM', max_length=10),
        ),
    ]