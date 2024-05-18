# Generated by Django 4.0.1 on 2024-04-04 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_alter_teacher_duties'),
    ]

    operations = [
        migrations.AddField(
            model_name='examslot',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_duties', to='teacher.teacher'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='duties',
            field=models.ManyToManyField(blank=True, related_name='teachers', to='teacher.ExamSlot'),
        ),
    ]
