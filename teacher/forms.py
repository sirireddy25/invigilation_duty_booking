from django import forms
from teacher.models import ExamSlot

class SignUpForm(forms.Form):
    college_id = forms.CharField(label='College ID', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ExamForm(forms.ModelForm):
    class Meta:
        model = ExamSlot
        fields = ['exam', 'date', 'start_time', 'end_time', 'room_number', 'semester']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class DateSemesterForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    SEMESTER_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
    ]
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES, widget=forms.RadioSelect)
