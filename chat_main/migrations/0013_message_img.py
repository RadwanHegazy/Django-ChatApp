# Generated by Django 3.1.5 on 2021-08-09 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_main', '0012_auto_20210808_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='static/chat-images/'),
        ),
    ]