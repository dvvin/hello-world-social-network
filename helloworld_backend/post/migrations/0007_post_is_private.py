# Generated by Django 5.0.1 on 2024-02-20 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_trend'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]