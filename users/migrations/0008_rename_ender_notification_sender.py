# Generated by Django 4.2.1 on 2023-06-05 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_sender_notification_ender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='ender',
            new_name='sender',
        ),
    ]
