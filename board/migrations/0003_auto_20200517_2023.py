# Generated by Django 3.0.6 on 2020-05-17 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='content',
            name='author',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
