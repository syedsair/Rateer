# Generated by Django 3.1.7 on 2021-08-09 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rating', models.FloatField()),
                ('RatedPid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings_rated_person', to=settings.AUTH_USER_MODEL)),
                ('RaterPid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ratings_rater_person', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Messenger', models.BooleanField(default=False)),
                ('Requests', models.BooleanField(default=False)),
                ('Feed', models.BooleanField(default=False)),
                ('ThisUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hobbies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hobby', models.CharField(max_length=254)),
                ('ThisUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Degree', models.CharField(max_length=254)),
                ('Institute', models.CharField(max_length=254, null=True)),
                ('From', models.DateField(null=True)),
                ('Till', models.DateField(null=True)),
                ('ThisUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
