from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Service(models.Model):
    """A service offered by the company, fully editable from Django Admin.

    Replaces the previously hardcoded SERVICES list in views.py so staff
    can add, edit, reorder, enable/disable, or remove services without any
    code changes.
    """

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    icon = models.CharField(
        max_length=60,
        default="code-braces",
        help_text=(
            "Material Design Icons name (without the 'mdi-' prefix), e.g. "
            "'code-braces'. Browse icons at pictogrammers.com/library/mdi/. "
            "Ignored if an image is uploaded below."
        ),
    )
    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True,
        help_text="Optional icon/image. If left blank, the icon name above is used.",
    )
    short_description = models.CharField(
        max_length=200,
        help_text="One or two sentences shown on the service card.",
    )
    description = models.TextField(
        blank=True,
        help_text="Optional longer description for a future service detail page.",
    )
    features = models.TextField(
        blank=True,
        help_text="Optional. One feature per line — shown as a bullet list.",
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first."
    )
    is_active = models.BooleanField(
        default=True, help_text="Untick to hide this service from the website."
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:140]
        super().save(*args, **kwargs)

    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]


class Course(models.Model):
    """A future / upcoming course, fully editable from Django Admin."""

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    icon = models.CharField(
        max_length=60,
        default="school-outline",
        help_text="Material Design Icons name (without the 'mdi-' prefix). Ignored if an image is uploaded.",
    )
    image = models.ImageField(upload_to="courses/", blank=True, null=True)
    short_description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional one-line summary shown on the course card.",
    )
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first."
    )
    is_active = models.BooleanField(
        default=True, help_text="Untick to hide this course from the website."
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:140]
        super().save(*args, **kwargs)


class ClientEnquiry(models.Model):
    """A lead captured through the public enquiry form.

    Kept intentionally simple: this is a contact/lead record, not a full
    CRM. Staff review and follow up on these from the Django admin.
    """

    class ServiceChoices(models.TextChoices):
        CUSTOM_SOFTWARE = "custom_software", "Custom Software Development"
        WEB_APP = "web_app", "Web Application Development"
        UI_UX = "ui_ux", "UI/UX Design"
        ERP_CRM = "erp_crm", "ERP / CRM Solutions"
        MAINTENANCE = "maintenance", "Maintenance & Support"
        CONSULTING = "consulting", "IT Consulting"
        AI_INTEGRATION = "ai_integration", "AI Integration"
        SEO_SERVICES = "seo_services", "SEO Services"
        STUDENT_PROJECTS = "student_projects", "College Student Projects"
        OTHER = "other", "Other / Not sure yet"

    class BudgetChoices(models.TextChoices):
        UNDER_5K = "under_5k", "Under $5,000"
        FIVE_TO_15K = "5k_15k", "$5,000 – $15,000"
        FIFTEEN_TO_50K = "15k_50k", "$15,000 – $50,000"
        OVER_50K = "over_50k", "$50,000+"
        NOT_SURE = "not_sure", "Not sure yet"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        IN_DISCUSSION = "in_discussion", "In discussion"
        WON = "won", "Won"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=120)
    company = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service_required = models.CharField(
        max_length=30, choices=ServiceChoices.choices, default=ServiceChoices.OTHER
    )
    budget = models.CharField(
        max_length=20, choices=BudgetChoices.choices, blank=True
    )
    project_description = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Client Enquiry"
        verbose_name_plural = "Client Enquiries"

    def __str__(self):
        return f"{self.name} — {self.get_service_required_display()}"
