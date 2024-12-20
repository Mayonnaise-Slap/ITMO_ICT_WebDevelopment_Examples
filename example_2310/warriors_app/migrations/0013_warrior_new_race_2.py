# Generated by Django 3.2.10 on 2024-09-27 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warriors_app', '0012_warrior_new_race'),
    ]

    operations = [
        migrations.AddField(
            model_name='warrior',
            name='new_race_2',
            field=models.CharField(blank=True, choices=[('s', 'student'), ('d', 'developer'), ('t', 'teamlead')], max_length=1, null=True, verbose_name='Новая Расса 2'),
        ),
    ]
