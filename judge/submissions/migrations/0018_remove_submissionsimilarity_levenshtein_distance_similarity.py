# Generated by Django 3.1.4 on 2021-07-03 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0017_auto_20210628_0537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissionsimilarity',
            name='levenshtein_distance_similarity',
        ),
    ]
