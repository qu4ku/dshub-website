# Generated by Django 2.0.6 on 2018-06-29 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_feed_url_feed'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='nooo', max_length=280),
            preserve_default=False,
        ),
    ]
