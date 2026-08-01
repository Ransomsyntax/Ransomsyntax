from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for RANSOM SYNTAX.
    role determines whether the account is a Student or a Teacher.
    Teacher accounts are created only by the Admin (via Django admin panel).
    Students self-register through the public registration page.
    """
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_TEACHER, 'Teacher'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    phone = models.CharField(max_length=20, blank=True)

    def is_student(self):
        return self.role == self.ROLE_STUDENT

    def is_teacher(self):
        return self.role == self.ROLE_TEACHER

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subject = models.CharField(max_length=150, blank=True, help_text="e.g. Data Science, Ethical Hacking")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name() or self.user.username}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Student: {self.user.get_full_name() or self.user.username}"
