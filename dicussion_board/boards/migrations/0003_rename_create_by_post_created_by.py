# Generated by Django 5.1 on 2024-08-29 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_rename_decription_board_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='create_by',
            new_name='created_by',
        ),
    ]
