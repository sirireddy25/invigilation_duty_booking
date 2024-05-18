from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    duties = models.ManyToManyField('ExamSlot', related_name='teachers', blank=True)

    def __str__(self):
        return self.user.username

class ExamSlot(models.Model):
    exam = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20, default='')
    semester = models.CharField(max_length=50, default='')
    booked = models.BooleanField(default=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assigned_duties', null=True, blank=True)

    def __str__(self):
        return f"{self.exam} - Sem {self.semester} - {self.date} - {self.start_time} - {self.end_time} - Room {self.room_number}"
