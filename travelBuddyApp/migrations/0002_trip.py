# Generated by Django 2.2.5 on 2019-09-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelBuddyApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dest', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=255)),
                ('travel_start', models.DateField()),
                ('travel_end', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
