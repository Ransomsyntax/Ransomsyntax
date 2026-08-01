import json
import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .forms import ClientEnquiryForm
from .models import Course, Service

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Content that drives the homepage sections. Services and Courses now come
# from the database (see models.Service / models.Course) and are managed
# entirely from Django Admin — no code changes needed to add, edit, reorder,
# or disable them. The rest of this editorial copy stays here since it
# changes with a code review, not something non-technical staff edit daily.
# ---------------------------------------------------------------------------

PROCESS_STEPS = [
    {
        "step": "01",
        "title": "Discovery",
        "description": "We study your goals, constraints, and users before a single line of code.",
    },
    {
        "step": "02",
        "title": "Design",
        "description": "Architecture and interface design reviewed with you before build begins.",
    },
    {
        "step": "03",
        "title": "Development",
        "description": "Iterative builds in short cycles, with visibility into progress throughout.",
    },
    {
        "step": "04",
        "title": "Quality Assurance",
        "description": "Manual and automated testing across devices, edge cases, and load.",
    },
    {
        "step": "05",
        "title": "Deployment",
        "description": "Controlled release with monitoring in place from day one.",
    },
    {
        "step": "06",
        "title": "Support",
        "description": "Ongoing maintenance, monitoring, and enhancement after launch.",
    },
]

TECHNOLOGIES = {
    "Frontend": ["React", "Vue.js", "TypeScript", "Bootstrap 5", "Tailwind CSS", "HTML5","CSS3","BOOTSTRAP" ],
    "Backend": ["Django", "Python", "Node.js", "REST & GraphQL APIs", "FLASK"],
    "Cloud & DevOps": ["AWS", "Azure", "Docker", "Kubernetes", "CI/CD"],
    "Data & AI": ["PostgreSQL", "Redis", "TensorFlow", "OpenAI API", "MYSQL"],
}

INDUSTRIES = [
    {"icon": "hospital-box-outline", "name": "Healthcare"},
    {"icon": "bank-outline", "name": "Finance & FinTech"},
    {"icon": "cart-outline", "name": "E-Commerce & Retail"},
    {"icon": "school-outline", "name": "Education & EdTech"},
    {"icon": "truck-delivery-outline", "name": "Logistics & Supply Chain"},
    {"icon": "home-city-outline", "name": "Real Estate"},
    {"icon": "shield-lock-outline", "name": "Cybersecurity"},
    {"icon": "factory", "name": "Manufacturing"},
]

TESTIMONIALS = [
    {
        "quote": "RansomSyntax rebuilt our internal platform without a single day of downtime. The communication throughout was exceptional.",
        "name": "Anita Sharma",
        "role": "Operations Director, sample placeholder client",
    },
    {
        "quote": "They caught architectural issues our previous vendor missed entirely, and fixed them before launch.",
        "name": "David Chen",
        "role": "CTO, sample placeholder client",
    },
    {
        "quote": "Professional, precise, and genuinely invested in getting the product right, not just shipped.",
        "name": "Fatima Al-Sayed",
        "role": "Founder, sample placeholder client",
    },
]

FAQS = [
    {
        "question": "What industries do you work with?",
        "answer": "We build for healthcare, finance, e-commerce, education, logistics, real estate, and more. Our process adapts to the compliance and scale needs of each sector.",
    },
    {
        "question": "How long does a typical project take?",
        "answer": "It depends on scope. A focused web application might take 6–10 weeks; an enterprise platform can run several months. We give a realistic timeline after discovery, before any contract is signed.",
    },
    {
        "question": "Do you offer ongoing support after launch?",
        "answer": "Yes. Every engagement can include a maintenance and support plan covering monitoring, patching, and incremental improvements.",
    },
    {
        "question": "Can you work with our existing codebase?",
        "answer": "Yes. We regularly audit, refactor, and extend existing systems rather than rebuilding from scratch when that's not necessary.",
    },
    {
        "question": "How do you handle project pricing?",
        "answer": "We scope work as fixed-price for well-defined projects or time-and-materials for evolving ones. You'll receive a clear proposal before work begins.",
    },
    {
        "question": "Is our data and source code kept confidential?",
        "answer": "Yes. We sign NDAs on request and follow standard secure development practices throughout the engagement.",
    },
]

# Placeholder responses for the chat widget. This is intentionally static —
# no external AI backend is wired up. See templates/website/includes/chat_widget.html
# for where an OpenAI/Anthropic-backed endpoint could be integrated later.
CHATBOT_RESPONSES = {
    "services": "We offer custom software, web & mobile development, UI/UX design, cloud solutions, API development, ERP/CRM systems, AI integration, and ongoing support. Which one are you exploring?",
    "pricing": "Pricing depends on scope — most engagements are quoted after a short discovery call. Want to share a few project details in our enquiry form?",
    "timeline": "Typical timelines range from 6 weeks for a focused web app to several months for an enterprise platform. Tell us about your project and we'll give you a realistic estimate.",
    "contact": f"You can reach us directly at {settings.SITE_CONTACT_EMAIL}, or fill out the enquiry form below and our team will follow up.",
    "default": "Thanks for your message. I'm a placeholder assistant for now — for a detailed answer, please use the enquiry form or email us at "
    f"{settings.SITE_CONTACT_EMAIL} and our team will get back to you personally.",
}


def home(request):
    """Single-page marketing site with an inline enquiry form."""
    if request.method == "POST":
        form = ClientEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            _notify_new_enquiry(enquiry)
            messages.success(
                request,
                "Thank you — your enquiry has been received. Our team will reach out shortly.",
            )
            return redirect(f"{reverse('website:home')}?enquiry=success#enquiry")
        else:
            messages.error(
                request, "Please correct the highlighted fields and try again."
            )
    else:
        form = ClientEnquiryForm()

    context = {
        "form": form,
        "services": Service.objects.filter(is_active=True),
        "courses": Course.objects.filter(is_active=True),
        "process_steps": PROCESS_STEPS,
        "technologies": TECHNOLOGIES,
        "industries": INDUSTRIES,
        "testimonials": TESTIMONIALS,
        "faqs": FAQS,
    }
    return render(request, "website/index.html", context)


def _notify_new_enquiry(enquiry):
    """Best-effort email notification. Never blocks the user-facing response."""
    try:
        send_mail(
            subject=f"New enquiry: {enquiry.name} ({enquiry.get_service_required_display()})",
            message=(
                f"Name: {enquiry.name}\n"
                f"Company: {enquiry.company or '—'}\n"
                f"Email: {enquiry.email}\n"
                f"Phone: {enquiry.phone or '—'}\n"
                f"Service: {enquiry.get_service_required_display()}\n"
                f"Budget: {enquiry.get_budget_display() if enquiry.budget else '—'}\n\n"
                f"Project description:\n{enquiry.project_description}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ENQUIRY_NOTIFICATION_EMAIL],
            fail_silently=True,
        )
    except Exception:  # pragma: no cover - notification failures must not break the UX
        logger.exception("Failed to send enquiry notification email")


def privacy_policy(request):
    return render(request, "website/privacy.html")


def terms_conditions(request):
    return render(request, "website/terms.html")


@require_POST
def chat_reply(request):
    """Placeholder chat endpoint for the AI help widget.

    Returns a canned response keyed off simple keyword matching. This is
    NOT an AI backend — it exists so the widget is functional out of the
    box. To wire up a real assistant, replace the body of this view with
    a call to your provider of choice (e.g. the Anthropic or OpenAI API)
    and keep the same JSON response shape: {"reply": "..."}.
    """
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        payload = {}

    message = (payload.get("message") or "").lower().strip()

    if any(word in message for word in ["price", "cost", "budget", "quote"]):
        reply = CHATBOT_RESPONSES["pricing"]
    elif any(word in message for word in ["service", "offer", "do you build", "capab"]):
        reply = CHATBOT_RESPONSES["services"]
    elif any(word in message for word in ["time", "long", "deadline", "when"]):
        reply = CHATBOT_RESPONSES["timeline"]
    elif any(word in message for word in ["contact", "email", "phone", "reach"]):
        reply = CHATBOT_RESPONSES["contact"]
    else:
        reply = CHATBOT_RESPONSES["default"]

    return JsonResponse({"reply": reply})


@require_GET
def sitemap_xml(request):
    """Minimal, dependency-free sitemap covering the site's public pages."""
    base = f"{request.scheme}://{request.get_host()}"
    urls = [
        {"loc": f"{base}{reverse('website:home')}", "priority": "1.0", "changefreq": "weekly"},
        {"loc": f"{base}{reverse('website:home')}#services", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base}{reverse('website:home')}#courses", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{base}{reverse('website:privacy_policy')}", "priority": "0.3", "changefreq": "yearly"},
        {"loc": f"{base}{reverse('website:terms_conditions')}", "priority": "0.3", "changefreq": "yearly"},
    ]
    xml = render_to_string("website/sitemap.xml", {"urls": urls})
    return HttpResponse(xml, content_type="application/xml")


@require_GET
def robots_txt(request):
    base = f"{request.scheme}://{request.get_host()}"
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {base}{reverse('website:sitemap_xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
