# Generated by Django 3.1.4 on 2021-07-03 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('code_tasks', '0012_tasktest_is_zero_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codetask',
            name='description_preview',
        ),
    ]
