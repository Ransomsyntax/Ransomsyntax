from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.student_register, name='student_register'),
    path('login/', views.student_login, name='student_login'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/edit-profile/', views.edit_profile, name='edit_profile'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]
