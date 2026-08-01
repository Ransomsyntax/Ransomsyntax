from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('enquiry/', views.enquiry_view, name='enquiry'),
    path('teacher/upload/', views.upload_video, name='upload_video'),
    path('teacher/video/<int:video_id>/edit/', views.edit_video, name='edit_video'),
    path('teacher/video/<int:video_id>/delete/', views.delete_video, name='delete_video'),
    path('teacher/video/<int:video_id>/access/', views.manage_access, name='manage_access'),
    path('teacher/course/<slug:slug>/students/', views.manage_students, name='manage_students'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
]
