# Generated by Django 5.0.1 on 2024-02-09 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_comment_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=255)),
                ('occurences', models.IntegerField()),
            ],
        ),
    ]
