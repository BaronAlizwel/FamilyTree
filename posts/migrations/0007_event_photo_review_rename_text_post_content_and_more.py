# Generated by Django 4.2.1 on 2023-06-12 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('posts', '0006_auto_20230612_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='posts.post')),
                ('event_date', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='posts.post')),
                ('image', models.ImageField(upload_to='photos/')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='posts.post')),
                ('rating', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='post',
            old_name='text',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='post',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='post',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('ST', 'Status'), ('EV', 'Event'), ('BL', 'Blog'), ('NW', 'News'), ('AL', 'Alert'), ('AN', 'Announcement'), ('PH', 'Photo'), ('VI', 'Video'), ('AR', 'Article'), ('RV', 'Review'), ('QU', 'Question'), ('OT', 'Others')], default='ST', max_length=2),
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('EV', 'Everyone'), ('FR', 'Friends'), ('CO', 'Connections'), ('PR', 'Private'), ('OT', 'Others')], default='EV', max_length=2),
        ),
    ]