from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Course, Video, VideoAccess, Enrollment, Enquiry
from .forms import EnquiryForm, VideoUploadForm, StudentAssignForm
from accounts.models import User


def course_list(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, slug):
    """
    Courses are browsable by everyone (marketing view), but a course is
    LOCKED for a student until a teacher or admin creates an Enrollment
    for them. Students cannot self-enroll. The Google Classroom link is
    only ever shown to students whose course is unlocked.
    """
    course = get_object_or_404(Course, slug=slug, is_active=True)
    videos = course.videos.all()

    unlocked_ids = []
    is_enrolled = False
    if request.user.is_authenticated and request.user.role == User.ROLE_STUDENT:
        unlocked_ids = list(VideoAccess.objects.filter(student=request.user, video__course=course)
                             .values_list('video_id', flat=True))
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    video_data = []
    for v in videos:
        can_watch = v.is_free or (v.id in unlocked_ids)
        video_data.append({'video': v, 'can_watch': can_watch})

    context = {
        'course': course,
        'video_data': video_data,
        'is_enrolled': is_enrolled,
        'is_locked': request.user.is_authenticated and request.user.role == User.ROLE_STUDENT and not is_enrolled,
    }
    return render(request, 'courses/course_detail.html', context)


def enquiry_view(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your enquiry has been received. Our team will contact you shortly.")
            return redirect('courses:enquiry')
    else:
        form = EnquiryForm()
    return render(request, 'courses/enquiry.html', {'form': form})


def _teacher_required(user):
    return user.is_authenticated and user.role == User.ROLE_TEACHER


@login_required(login_url='accounts:teacher_login')
def upload_video(request):
    if not _teacher_required(request.user):
        messages.error(request, "Only teachers can upload videos.")
        return redirect('accounts:student_dashboard')

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES, teacher=request.user)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            messages.success(request, f"Video '{video.title}' uploaded successfully.")
            return redirect('accounts:teacher_dashboard')
    else:
        form = VideoUploadForm(teacher=request.user)
    return render(request, 'courses/upload_video.html', {'form': form})


@login_required(login_url='accounts:teacher_login')
def edit_video(request, video_id):
    if not _teacher_required(request.user):
        messages.error(request, "Only teachers can edit videos.")
        return redirect('accounts:student_dashboard')
    video = get_object_or_404(Video, id=video_id, uploaded_by=request.user)
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, "Video updated successfully.")
            return redirect('accounts:teacher_dashboard')
    else:
        form = VideoUploadForm(instance=video)
    return render(request, 'courses/upload_video.html', {'form': form, 'editing': True, 'video': video})


@login_required(login_url='accounts:teacher_login')
def delete_video(request, video_id):
    if not _teacher_required(request.user):
        messages.error(request, "Only teachers can delete videos.")
        return redirect('accounts:student_dashboard')
    video = get_object_or_404(Video, id=video_id, uploaded_by=request.user)
    if request.method == 'POST':
        video.delete()
        messages.success(request, "Video deleted.")
        return redirect('accounts:teacher_dashboard')
    return render(request, 'courses/confirm_delete.html', {'video': video})


@login_required(login_url='accounts:teacher_login')
def manage_access(request, video_id):
    """Teacher grants or revokes individual student access to a paid video."""
    if not _teacher_required(request.user):
        messages.error(request, "Only teachers can manage video access.")
        return redirect('accounts:student_dashboard')
    video = get_object_or_404(Video, id=video_id, uploaded_by=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username', '').strip()
        if action == 'grant' and username:
            try:
                student = User.objects.get(username=username, role=User.ROLE_STUDENT)
                VideoAccess.objects.get_or_create(video=video, student=student, defaults={'granted_by': request.user})
                messages.success(request, f"Access granted to {student.username}.")
            except User.DoesNotExist:
                messages.error(request, f"No student found with username '{username}'.")
        elif action == 'revoke':
            access_id = request.POST.get('access_id')
            VideoAccess.objects.filter(id=access_id, video=video).delete()
            messages.info(request, "Access revoked.")
        return redirect('courses:manage_access', video_id=video.id)

    grants = video.access_grants.select_related('student').all()
    return render(request, 'courses/manage_access.html', {'video': video, 'grants': grants})


@login_required(login_url='accounts:teacher_login')
def manage_students(request, slug):
    """
    Teacher-only: unlock or lock a student's access (Enrollment) to ONE of
    the teacher's own courses. Teachers can never touch a course they are
    not assigned to.
    """
    if not _teacher_required(request.user):
        messages.error(request, "Only teachers can manage students.")
        return redirect('accounts:student_dashboard')

    course = get_object_or_404(Course, slug=slug, teachers=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'assign':
            form = StudentAssignForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                try:
                    student = User.objects.get(username=username, role=User.ROLE_STUDENT)
                    Enrollment.objects.get_or_create(student=student, course=course)
                    messages.success(request, f"Unlocked '{course.title}' for {student.username}.")
                except User.DoesNotExist:
                    messages.error(request, f"No student found with username '{username}'.")
        elif action == 'remove':
            enrollment_id = request.POST.get('enrollment_id')
            Enrollment.objects.filter(id=enrollment_id, course=course).delete()
            messages.info(request, "Access locked for that student.")
        return redirect('courses:manage_students', slug=course.slug)

    form = StudentAssignForm()
    enrollments = Enrollment.objects.filter(course=course).select_related('student').order_by('student__username')
    return render(request, 'courses/manage_students.html', {
        'course': course, 'form': form, 'enrollments': enrollments,
    })
