# Generated by Django 4.0.1 on 2024-04-02 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examslot',
            name='room_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]
