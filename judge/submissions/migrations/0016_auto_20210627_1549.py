# Generated by Django 3.1.4 on 2021-06-27 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0015_auto_20210626_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='processing_state',
            field=models.CharField(choices=[('NOT_STARTED', 'NOT_STARTED'), ('ENQUEUE_FOR_JUDGING', 'ENQUEUE_FOR_JUDGING'), ('JUDGING_IN_PROGRESS', 'JUDGING_IN_PROGRESS'), ('JUDGED', 'JUDGED')], default='ENQUEUE_FOR_JUDGING', max_length=19),
        ),
    ]
