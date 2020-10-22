# Generated by Django 3.1.2 on 2020-10-22 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warriors_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warrior',
            name='level',
            field=models.IntegerField(default=0, verbose_name='Уровень'),
        ),
        migrations.AlterField(
            model_name='warrior',
            name='profession',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warriors_app.profession', verbose_name='Профессия'),
        ),
        migrations.AlterField(
            model_name='warrior',
            name='race',
            field=models.CharField(choices=[('s', 'student'), ('d', 'developer'), ('t', 'teamlead')], max_length=1, verbose_name='Расса'),
        ),
    ]