from django.contrib import admin
from .models import ExamSlot, Teacher

admin.site.register(ExamSlot)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_duties')  #the fields to display in the teacher list

    def get_duties(self, obj):
        # Get the duties associated with the teacher and return a comma-separated string
        return ', '.join(str(duty) for duty in obj.duties.all())

    get_duties.short_description = 'Duties' 

admin.site.register(Teacher, TeacherAdmin)
