from django.contrib import admin
from .models import Course, Video, VideoAccess, Enrollment, Enquiry


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'mode', 'is_active', 'teacher_list', 'free_video_count', 'paid_video_count', 'created_at')
    list_filter = ('mode', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    filter_horizontal = ('teachers',)

    def teacher_list(self, obj):
        return ", ".join(t.get_full_name() or t.username for t in obj.teachers.all()) or "—"
    teacher_list.short_description = "Assigned teacher(s)"


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_by', 'is_free', 'order', 'created_at')
    list_filter = ('is_free', 'course')
    search_fields = ('title', 'course__title', 'uploaded_by__username')


@admin.register(VideoAccess)
class VideoAccessAdmin(admin.ModelAdmin):
    list_display = ('video', 'student', 'granted_by', 'granted_at')
    search_fields = ('video__title', 'student__username')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    This is how Admin (or a Teacher, from their dashboard) grants a student
    access ('unlocks') a course. A student with no Enrollment row for a
    course sees that course as locked and cannot self-enroll.
    """
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course',)
    search_fields = ('student__username', 'course__title')
    autocomplete_fields = ('student', 'course')


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'course_interested', 'is_contacted', 'created_at')
    list_filter = ('is_contacted', 'course_interested')
    search_fields = ('name', 'email', 'phone')
