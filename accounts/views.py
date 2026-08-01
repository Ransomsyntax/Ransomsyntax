from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import StudentRegistrationForm, BootstrapAuthenticationForm, StudentProfileEditForm
from .models import User, StudentProfile
from courses.models import Course, Video, VideoAccess, Enrollment


def student_register(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to RANSOM SYNTAX, {user.first_name}! Your student account is ready.")
            return redirect('accounts:student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/student_register.html', {'form': form})


def student_login(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = BootstrapAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role != User.ROLE_STUDENT:
                messages.error(request, "This login is for students only. Teachers please use the Teacher Login page.")
            else:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('accounts:student_dashboard')
    else:
        form = BootstrapAuthenticationForm()
    return render(request, 'accounts/student_login.html', {'form': form})


def teacher_login(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = BootstrapAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role != User.ROLE_TEACHER:
                messages.error(request, "This login is for teachers only. Students please use the Student Login page.")
            else:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('accounts:teacher_dashboard')
    else:
        form = BootstrapAuthenticationForm()
    return render(request, 'accounts/teacher_login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('core:home')


@login_required(login_url='accounts:student_login')
def student_dashboard(request):
    if request.user.role != User.ROLE_STUDENT:
        messages.error(request, "Only students can access this dashboard.")
        return redirect('accounts:teacher_dashboard')

    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    # Only courses a teacher or admin has unlocked for this student ('My Courses').
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    enrolled_course_ids = list(enrollments.values_list('course_id', flat=True))
    # Everything else is shown as locked/browsable, but students cannot self-enroll here.
    locked_courses = Course.objects.filter(is_active=True).exclude(id__in=enrolled_course_ids)
    unlocked_video_ids = VideoAccess.objects.filter(student=request.user).values_list('video_id', flat=True)

    context = {
        'profile': profile,
        'enrollments': enrollments,
        'enrolled_course_ids': enrolled_course_ids,
        'locked_courses': locked_courses,
        'unlocked_video_ids': list(unlocked_video_ids),
    }
    return render(request, 'accounts/student_dashboard.html', context)


@login_required(login_url='accounts:student_login')
def edit_profile(request):
    if request.user.role != User.ROLE_STUDENT:
        return redirect('accounts:teacher_dashboard')
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StudentProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:student_dashboard')
    else:
        form = StudentProfileEditForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required(login_url='accounts:teacher_login')
def teacher_dashboard(request):
    if request.user.role != User.ROLE_TEACHER:
        messages.error(request, "Only teachers can access this dashboard.")
        return redirect('accounts:student_dashboard')

    videos = Video.objects.filter(uploaded_by=request.user).select_related('course').order_by('-created_at')
    # A teacher only ever manages the courses Admin has assigned to them.
    courses = Course.objects.filter(is_active=True, teachers=request.user)
    context = {
        'videos': videos,
        'courses': courses,
    }
    return render(request, 'accounts/teacher_dashboard.html', context)
