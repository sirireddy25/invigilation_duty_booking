from django.urls import path
from . import views

urlpatterns = [
    path('exam-schedule/', views.exam_schedule, name='exam_schedule'),
    path('duties/', views.duties, name='duties'),
    path('signup/', views.signup, name='signup'),
    path('', views.user_login, name='login'),  
    path('logout/', views.logout_view, name='logout'),

    #admin views
    path('add-exam/', views.add_exam, name='add_exam'),
    path('view-teachers/', views.view_teachers, name='view_teachers'),
    path('view-exams/', views.view_exams, name='view_exams'),
]
