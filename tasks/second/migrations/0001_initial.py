# Generated by Django 4.1.7 on 2023-03-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RateDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cur_id', models.PositiveIntegerField()),
                ('data', models.JSONField()),
            ],
        ),
    ]
