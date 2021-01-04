# Generated by Django 3.1.4 on 2021-01-07 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0007_submission_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='processing_state',
            field=models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('ENQUEUE_FOR_JUDGING', 'ENQUEUE_FOR_JUDGING'), ('PROCESSED', 'PROCESSED')], default='NOT_STARTED', max_length=19),
        ),
    ]
