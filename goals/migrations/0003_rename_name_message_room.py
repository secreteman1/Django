# Generated by Django 4.1.7 on 2024-02-05 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_topic_room_host_message_room_topic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='name',
            new_name='room',
        ),
    ]
