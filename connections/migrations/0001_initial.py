# Generated by Django 4.2.1 on 2023-06-03 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_type', models.CharField(choices=[('PR', 'Parent'), ('CH', 'Child'), ('SB', 'Sibling')], max_length=2)),
            ],
        ),
    ]
