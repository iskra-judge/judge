# Generated by Django 3.1.4 on 2021-01-07 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_tasks', '0006_codetask_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='codetaskcategory',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AddField(
            model_name='codetask',
            name='description_preview',
            field=models.TextField(blank=True),
        ),
    ]