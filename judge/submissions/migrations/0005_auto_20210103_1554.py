# Generated by Django 3.1.4 on 2021-01-03 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0004_auto_20210102_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissiontestresulttype',
            name='name',
            field=models.CharField(choices=[('Correct Answer', 'Correct Answer'), ('Wrong Answer', 'Wrong Answer'), ('Execution Error', 'Execution Error'), ('Unknown', 'Unknown')], default='Unknown', max_length=15),
        ),
    ]
