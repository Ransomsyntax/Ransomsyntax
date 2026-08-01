from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html

from .models import ClientEnquiry, Course, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "icon", "order", "is_active", "updated_at")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    search_fields = ("title", "short_description", "description")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
    fieldsets = (
        (None, {"fields": ("title", "slug", "is_active", "order")}),
        ("Icon / Image", {"fields": ("icon", "image")}),
        ("Content", {"fields": ("short_description", "description", "features")}),
    )

    @admin.display(description="")
    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:32px;height:32px;object-fit:cover;border-radius:6px;">',
                obj.image.url,
            )
        return format_html(
            '<i class="mdi mdi-{}" style="font-size:20px;"></i>', obj.icon
        )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "icon", "order", "is_active", "updated_at")
    list_display_links = ("title",)
    list_editable = ("order", "is_active")
    search_fields = ("title", "short_description", "description")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")

    @admin.display(description="")
    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:32px;height:32px;object-fit:cover;border-radius:6px;">',
                obj.image.url,
            )
        return format_html(
            '<i class="mdi mdi-{}" style="font-size:20px;"></i>', obj.icon
        )


@admin.register(ClientEnquiry)
class ClientEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "email",
        "phone",
        "service_required",
        "budget",
        "status",
        "created_at",
    )
    list_filter = ("status", "service_required", "budget", "created_at")
    search_fields = ("name", "company", "email", "phone", "project_description")
    list_editable = ("status",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


# ---------------------------------------------------------------------------
# Admin dashboard: adds summary statistics to the default admin index page
# (Total Services, Total Courses, Total Messages, Recent Enquiries) without
# replacing Django's built-in admin. See templates/admin/index.html for the
# matching template override.
# ---------------------------------------------------------------------------
_original_index = AdminSite.index


def _dashboard_index(self, request, extra_context=None):
    extra_context = extra_context or {}
    extra_context.update(
        {
            "rs_total_services": Service.objects.count(),
            "rs_active_services": Service.objects.filter(is_active=True).count(),
            "rs_total_courses": Course.objects.count(),
            "rs_active_courses": Course.objects.filter(is_active=True).count(),
            "rs_total_messages": ClientEnquiry.objects.count(),
            "rs_new_messages": ClientEnquiry.objects.filter(status="new").count(),
            "rs_recent_enquiries": ClientEnquiry.objects.order_by("-created_at")[:6],
        }
    )
    return _original_index(self, request, extra_context)


admin.site.index = _dashboard_index.__get__(admin.site, AdminSite)
admin.site.site_header = "RansomSyntax Admin"
admin.site.site_title = "RansomSyntax Admin"
admin.site.index_title = "Dashboard"
