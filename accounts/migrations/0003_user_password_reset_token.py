# Generated by Django 4.1 on 2023-08-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_email_token_user_is_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_reset_token',
            field=models.BooleanField(blank=True, max_length=250, null=True),
        ),
    ]