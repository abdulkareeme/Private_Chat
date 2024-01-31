# Generated by Django 4.2.1 on 2024-01-27 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_user_last_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='confirmation_tries',
            field=models.IntegerField(blank=True, default=3),
        ),
        migrations.AddField(
            model_name='user',
            name='next_confirm_try',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='next_confirmation_code_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='resend_tries',
            field=models.IntegerField(blank=True, default=3),
        ),
    ]