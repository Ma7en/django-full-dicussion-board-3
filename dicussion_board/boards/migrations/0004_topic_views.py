# Generated by Django 5.1 on 2024-08-30 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_rename_create_by_post_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
