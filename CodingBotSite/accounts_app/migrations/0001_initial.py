# Generated by Django 2.0.3 on 2018-04-06 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=500)),
                ('lastName', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=700)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolName', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=700)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=500)),
                ('lastName', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=700)),
                ('schoolID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts_app.School')),
            ],
        ),
        migrations.AddField(
            model_name='professor',
            name='schoolID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts_app.School'),
        ),
    ]