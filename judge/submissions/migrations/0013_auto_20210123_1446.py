# Generated by Django 3.1.4 on 2021-01-23 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0012_submissionsimilarity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissiontestresulttype',
            name='name',
            field=models.CharField(choices=[('Correct Answer', 'Correct Answer'), ('Wrong Answer', 'Wrong Answer'), ('Execution Error', 'Execution Error'), ('Unknown', 'Unknown'), ('Time Limit', 'Time Limit'), ('Memory Limit', 'Memory Limit')], default='Unknown', max_length=15),
        ),
    ]