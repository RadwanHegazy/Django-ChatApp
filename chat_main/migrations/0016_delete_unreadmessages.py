# Generated by Django 3.1.5 on 2021-08-17 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_main', '0015_unreadmessages'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UnreadMessages',
        ),
    ]
