# Generated by Django 3.1.4 on 2021-01-05 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_tasks', '0002_auto_20210103_1840'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codetask',
            old_name='description',
            new_name='description_md',
        ),
        migrations.AddField(
            model_name='codetask',
            name='description_html',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
