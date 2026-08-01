from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-conditions/", views.terms_conditions, name="terms_conditions"),
    path("api/chat/", views.chat_reply, name="chat_reply"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
