# Generated by Django 3.2.16 on 2022-11-15 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_recipie'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Recipie',
            new_name='Recipe',
        ),
    ]