from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm, ExamForm, DateSemesterForm
from .models import ExamSlot, Teacher

def signup(request):
    error = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            college_id = form.cleaned_data['college_id']
            password = form.cleaned_data['password']
            if User.objects.filter(username=college_id).exists():
                error = "Username already exists"
            else:
                user = User.objects.create_user(username=college_id, password=password)
                user.save()
                teacher = Teacher.objects.create(user=user)
                login(request, user)
                return redirect('exam_schedule')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'error': error})

def user_login(request):
    error = None
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
                else:
                    return redirect('exam_schedule')
            else:
                error = "Invalid username or password"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

def exam_schedule(request):
    x = 0
    teacher = request.user.teacher

    num_duties = teacher.duties.all().count()
    progress = (num_duties/4) * 100
    if progress > 100:
        progress = 100
    
    sort_by = request.GET.get('sort_by', 'date')
    exams = ExamSlot.objects.all()

    if request.method == 'GET':
        if sort_by == 'semester':
            exams = exams.order_by('semester')
        else:
            exams = exams.order_by('date', 'start_time')
        return render(request, 'exam_schedule.html', {'exams': exams, 'x': x, 'progress':progress, 'num_duties':num_duties})
    
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
           return render(request, 'exam_schedule.html', {'exams': exams, 'x': x, 'progress':progress, 'num_duties':num_duties})
        else:
            for slot in selected_slots:
                slot.booked = True
                slot.save()
                teacher = request.user.teacher
                slot.teacher = teacher
                slot.save()
                teacher.duties.add(slot)
                teacher.save()
            return render(request, 'exam_schedule.html', {'exams': exams, 'x': x, 'progress':progress, 'num_duties':num_duties})


from django.contrib.auth.decorators import login_required

@login_required
def duties(request):
    teacher = request.user.teacher
    duties = teacher.duties.all().order_by('date', 'start_time') if teacher else []
    
    # Debug print statement
    print("Duties:", duties)
    for duty in duties:
        print(f"Duty: {duty.exam}, Date: {duty.date}, Start: {duty.start_time}, End: {duty.end_time}, Room: {duty.room_number}")

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


from django.shortcuts import render
from .models import ExamSlot
from .forms import DateSemesterForm

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

