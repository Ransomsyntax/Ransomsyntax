from django.conf import settings


def site_info(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
        'SITE_YOUTUBE_URL': settings.SITE_YOUTUBE_URL,
        'SITE_INSTAGRAM_URL': settings.SITE_INSTAGRAM_URL,
    }
