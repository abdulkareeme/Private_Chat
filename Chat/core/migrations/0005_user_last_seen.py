# Generated by Django 4.2.1 on 2023-12-30 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_chatkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_seen',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
