from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Course(models.Model):
    MODE_ONLINE = 'online'
    MODE_OFFLINE = 'offline'
    MODE_BOTH = 'both'

    MODE_CHOICES = [
        (MODE_ONLINE, 'Online'),
        (MODE_OFFLINE, 'Offline'),
        (MODE_BOTH, 'Online & Offline'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)

    mode = models.CharField(
        max_length=10,
        choices=MODE_CHOICES,
        default=MODE_BOTH
    )

    is_active = models.BooleanField(default=True)

    # NEW FIELDS
    classroom_url = models.URLField(blank=True, null=True)
    classroom_code = models.CharField(max_length=50, blank=True, null=True)

    teachers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='teaching_courses', blank=True,
        limit_choices_to={'role': 'teacher'},
        help_text="Teacher(s) who own/manage this course. Set by Admin."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def free_video_count(self):
        return self.videos.filter(is_free=True).count()

    def paid_video_count(self):
        return self.videos.filter(is_free=False).count()
    
class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_videos',
        limit_choices_to={'role': 'teacher'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True,
                                   help_text="Upload a video file (optional if using an external URL below).")
    external_url = models.URLField(blank=True, help_text="Optional: YouTube/Vimeo embed link instead of a file upload.")
    is_free = models.BooleanField(default=False, help_text="If checked, ALL students can watch this video for free.")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    youtube_url = models.URLField(blank=True, null=True)
    is_free = models.BooleanField(default=False)
    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class VideoAccess(models.Model):
    """Grants an individual student access to one specific paid video."""
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='access_grants')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_accesses',
                                 limit_choices_to={'role': 'student'})
    granted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='granted_accesses', limit_choices_to={'role': 'teacher'})
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'student')

    def __str__(self):
        return f"{self.student.username} -> {self.video.title}"


class Enrollment(models.Model):
    """A student selecting/following a course."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments',
                                 limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class Enquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course_interested = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f"{self.name} - {self.email}"
