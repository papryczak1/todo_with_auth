# Generated by Django 3.0.5 on 2020-04-18 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='dateCompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
