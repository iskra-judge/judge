# Generated by Django 3.1.4 on 2021-01-21 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_tasks', '0010_auto_20210109_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='codetask',
            name='memory_limit_in_bytes',
            field=models.IntegerField(default=16),
        ),
        migrations.AddField(
            model_name='codetask',
            name='time_limit_in_ms',
            field=models.IntegerField(default=100),
        ),
    ]