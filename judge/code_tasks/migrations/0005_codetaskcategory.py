# Generated by Django 3.1.4 on 2021-01-07 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_tasks', '0004_auto_20210107_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeTaskCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
    ]
