# Generated by Django 3.1.5 on 2021-02-06 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grudapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'permissions': [('add', 'Can change the status of tasks'), ('delete', 'Can remove a task by setting its status as closed')]},
        ),
    ]
