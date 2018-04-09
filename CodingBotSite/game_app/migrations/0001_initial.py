# Generated by Django 2.0.3 on 2018-04-06 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2000)),
                ('fininshed', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('probQuestion', models.CharField(max_length=2000)),
                ('probAnswer', models.CharField(max_length=1000)),
                ('story', models.CharField(max_length=5000)),
                ('packId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_app.Pack')),
            ],
        ),
    ]