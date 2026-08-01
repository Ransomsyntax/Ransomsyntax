from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts import views as accounts_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # ------------------------------------------------------------------
    # Education platform ("For Students"), mounted under /students/.
    # Each app keeps its ORIGINAL namespace (core, accounts, courses,
    # chatbot) and its templates are completely unchanged — only the URL
    # prefix is new. Because {% url %} tags resolve by namespace (not by
    # prefix), every existing link/form/redirect in the education
    # templates keeps working with zero code changes.
    #
    #   /students/                -> core:home
    #   /students/about/          -> core:about
    #   /students/login/          -> accounts:student_login
    #   /students/register/       -> accounts:student_register
    #   /students/dashboard/      -> accounts:student_dashboard
    #   /students/profile/        -> accounts:edit_profile (alias, see below)
    #   /students/courses/        -> courses:course_list
    #   /students/courses/<slug>/ -> courses:course_detail
    # ------------------------------------------------------------------
    path("students/", include("core.urls")),
    path("students/", include("accounts.urls")),
    path("students/courses/", include("courses.urls")),
    path("students/chatbot/", include("chatbot.urls")),

    # Friendly alias so /students/profile/ works exactly as requested,
    # without changing the existing accounts:edit_profile view or the
    # original /students/dashboard/edit-profile/ URL it already has.
    path("students/profile/", accounts_views.edit_profile, name="student_profile_alias"),

    # Main marketing website stays mounted at the site root and keeps
    # every existing URL (/, /privacy-policy/, /terms-conditions/, etc.)
    # completely unchanged.
    path("", include("website.urls", namespace="website")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
