from django.shortcuts import render
from courses.models import Course, Video


def home(request):
    courses = Course.objects.filter(is_active=True)[:6]
    free_videos = Video.objects.filter(is_free=True).select_related('course')[:6]
    context = {
        'courses': courses,
        'free_videos': free_videos,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')
