from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm, ExamForm, DateSemesterForm
from .models import ExamSlot, Teacher

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            college_id = form.cleaned_data['college_id']
            password = form.cleaned_data['password']
            # Check if the user already exists
            if User.objects.filter(username=college_id).exists():
                # Handle case where user already exists
                pass
            else:
                # Create new user
                
                user = User.objects.create_user(username=college_id, password=password)
                #user.is_staff = True 
                user.save()
                teacher = Teacher.objects.create(user=user)
                # Log in the user
                login(request, user)
                return redirect('exam_schedule')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                if user.is_superuser:
                    return redirect('add_exam')
                # Redirect other users to the application's home page
                else:
                    return redirect('exam_schedule')
            else:
                # Authentication failed, handle error
                pass
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def exam_schedule(request):
    x = 0
    sort_by = request.GET.get('sort_by', 'date')
    exams = ExamSlot.objects.all()

    if request.method == 'GET':
        if sort_by == 'semester':
            exams = exams.order_by('semester')
        else:
            exams = exams.order_by('date', 'start_time')
        return render(request, 'exam_schedule.html', {'exams': exams, 'x': x})
    
    elif request.method == 'POST':
        selected_slot_ids = request.POST.getlist('selected_slots')
        selected_slots = ExamSlot.objects.filter(id__in=selected_slot_ids)

        existing_bookings = ExamSlot.objects.filter(
            teacher=request.user.teacher, 
            date__in=[slot.date for slot in selected_slots],
            start_time__in=[slot.start_time for slot in selected_slots]
        )
        
        if existing_bookings.exists():
           x = 1
           return render(request, 'exam_schedule.html', {'exams': exams, 'x': x})
        else:
            for slot in selected_slots:
                slot.booked = True
                slot.save()
                teacher = request.user.teacher
                slot.teacher = teacher
                slot.save()
                teacher.duties.add(slot)
                teacher.save()
            return render(request, 'exam_schedule.html', {'exams': exams, 'x': x})

def duties(request):
    # Get the current user's teacher object
    teacher = request.user.teacher

    # Retrieve duties for the teacher
    if teacher:
        duties = teacher.duties.all()
        duties = duties.order_by('date', 'start_time')
    else:
        duties = []

    # Render the template with the duties
    return render(request, 'duties.html', {'duties': duties})


#admin
def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_exams')
    else:
        form = ExamForm()
    return render(request, 'add_exam.html', {'form': form})


def view_exams(request):
    exams = ExamSlot.objects.all().order_by('semester', 'start_time')
    return render(request, 'view_exams.html', {'exams': exams})


def view_teachers(request):
    if request.method == 'POST':
        form = DateSemesterForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            semester = form.cleaned_data['semester']
            # Fetch exam slots based on date and semester
            exam_slots = ExamSlot.objects.filter(date=date, semester=semester).order_by('start_time')
            return render(request, 'view_teachers.html', {
                'form': form,
                'exam_slots': exam_slots,
                'selected_date': date,
                'selected_semester': semester,
            })
    else:
        form = DateSemesterForm()
    return render(request, 'view_teachers.html', {'form': form})
