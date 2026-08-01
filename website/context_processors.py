from django.conf import settings


def site_settings(request):
    """Expose company profile constants to every template.

    Avoids repeating the contact email, social links, etc. in every view.
    """
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_TAGLINE": settings.SITE_TAGLINE,
        "SITE_CONTACT_EMAIL": settings.SITE_CONTACT_EMAIL,
        "SITE_YOUTUBE_URL": settings.SITE_YOUTUBE_URL,
        "SITE_INSTAGRAM_URL": settings.SITE_INSTAGRAM_URL,
    }
