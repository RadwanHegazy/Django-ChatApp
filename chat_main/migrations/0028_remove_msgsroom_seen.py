# Generated by Django 3.1.5 on 2021-08-24 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat_main', '0027_auto_20210824_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='msgsroom',
            name='seen',
        ),
    ]
