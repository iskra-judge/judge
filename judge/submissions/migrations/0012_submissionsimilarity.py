# Generated by Django 3.1.4 on 2021-01-21 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0011_auto_20210107_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionSimilarity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jaccard_similarity', models.IntegerField()),
                ('lcs_similarity', models.IntegerField()),
                ('cosine_similarity', models.IntegerField()),
                ('submission1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions1', to='submissions.submission')),
                ('submission2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions2', to='submissions.submission')),
            ],
        ),
    ]
