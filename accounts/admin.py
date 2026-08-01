from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TeacherProfile, StudentProfile

admin.site.site_header = "Ransom Syntax Administration"
admin.site.site_title = "Ransom Syntax Admin"
admin.site.index_title = "Welcome to Ransom Syntax Admin Panel"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin can create Teacher accounts here by setting role = Teacher.
    Students normally self-register, but admin can also manage them here.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('RANSOM SYNTAX Role', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('RANSOM SYNTAX Role', {'fields': ('role', 'phone', 'email')}),
    )


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject')
    search_fields = ('user__username', 'user__first_name', 'subject')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'phone')
