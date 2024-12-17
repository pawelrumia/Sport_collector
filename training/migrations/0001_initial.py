# Generated by Django 5.1.4 on 2024-12-16 20:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('sport', models.CharField(choices=[('running', 'Running'), ('swimming', 'Swimming'), ('pullups', 'Pull-ups'), ('cycling', 'Cycling'), ('pushups', 'Push-ups'), ('weights', 'Weights')], max_length=50)),
                ('details', models.JSONField()),
                ('calories_burned', models.FloatField()),
            ],
        ),
    ]
