from django.db import migrations

SERVICES = [
    {
        "title": "Custom Software Development",
        "icon": "code-braces",
        "short_description": "Bespoke systems engineered around your workflows, not the other way around.",
        "features": "Requirements-driven architecture\nScalable, maintainable codebases\nDirect access to the engineering team",
        "order": 10,
    },
    {
        "title": "Web Application Development",
        "icon": "web",
        "short_description": "Fast, secure, and scalable web platforms built on modern frameworks.",
        "features": "Responsive, accessible interfaces\nDjango / React / modern stacks\nPerformance-tuned from day one",
        "order": 20,
    },
    {
        "title": "UI/UX Design",
        "icon": "palette-swatch",
        "short_description": "Interfaces designed around real user behaviour — clean, intuitive, on-brand.",
        "features": "User research & wireframes\nDesign systems\nUsability-tested prototypes",
        "order": 30,
    },
    {
        "title": "API Development",
        "icon": "api",
        "short_description": "Well-documented, versioned APIs built for integration at scale.",
        "features": "REST & GraphQL\nAuthentication & rate limiting\nClear developer documentation",
        "order": 40,
    },
    {
        "title": "ERP / CRM Solutions",
        "icon": "office-building-cog-outline",
        "short_description": "Operational systems that unify sales, ops, and reporting in one place.",
        "features": "Custom workflows\nRole-based access\nReporting dashboards",
        "order": 50,
    },
    {
        "title": "IT Consulting",
        "icon": "lightbulb-on-outline",
        "short_description": "Independent technical guidance on architecture, stack, and roadmap.",
        "features": "Architecture review\nTechnology roadmap\nVendor-neutral advice",
        "order": 60,
    },
    {
        "title": "AI Integration",
        "icon": "creation",
        "short_description": "Practical AI features — automation, retrieval, and assistants — shipped responsibly.",
        "features": "Chat & retrieval assistants\nWorkflow automation\nResponsible deployment practices",
        "order": 70,
    },
    {
        "title": "SEO Services",
        "icon": "chart-line",
        "short_description": "Technical and on-page SEO that helps your site rank and load fast.",
        "features": "Technical SEO audits\nOn-page optimisation\nStructured data & performance tuning",
        "order": 80,
    },
    {
        "title": "College Student Projects",
        "icon": "school-outline",
        "short_description": "Guided academic and mini/major projects for engineering and diploma students.",
        "features": "Project guidance & mentorship\nSource code & documentation\nViva / presentation support",
        "order": 90,
    },
]

COURSES = [
    ("Cloud Computing", "cloud-outline"),
    ("DevOps", "infinity"),
    ("React", "react"),
    ("Flutter", "cellphone-cog"),
    ("Java", "language-java"),
    ("MERN Stack", "layers-triple-outline"),
    ("Data Engineering", "database-cog-outline"),
    ("Artificial Intelligence", "robot-outline"),
    ("Machine Learning", "chart-scatter-plot"),
    ("Cyber Security", "shield-lock-outline"),
]


def seed(apps, schema_editor):
    Service = apps.get_model("website", "Service")
    Course = apps.get_model("website", "Course")
    from django.utils.text import slugify

    for data in SERVICES:
        if not Service.objects.filter(title=data["title"]).exists():
            Service.objects.create(
                title=data["title"],
                slug=slugify(data["title"]),
                icon=data["icon"],
                short_description=data["short_description"],
                features=data["features"],
                order=data["order"],
                is_active=True,
            )

    for i, (title, icon) in enumerate(COURSES, start=1):
        if not Course.objects.filter(title=title).exists():
            Course.objects.create(
                title=title,
                slug=slugify(title),
                icon=icon,
                short_description=f"Upcoming course — {title} training and mentorship.",
                order=i * 10,
                is_active=True,
            )


def unseed(apps, schema_editor):
    Service = apps.get_model("website", "Service")
    Course = apps.get_model("website", "Course")
    Service.objects.filter(title__in=[s["title"] for s in SERVICES]).delete()
    Course.objects.filter(title__in=[c[0] for c in COURSES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0002_course_service_alter_clientenquiry_service_required"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
