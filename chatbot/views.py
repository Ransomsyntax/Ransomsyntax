import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.conf import settings

from courses.models import Course

# Simple keyword -> reply rules for the student-friendly help chatbot.
# Each rule: (list of keywords, reply text, optional link)
RULES = [
    (['hi', 'hello', 'hey', 'hii'],
     "Hi there! 👋 I'm the RANSOM SYNTAX assistant. Ask me about our courses, fees, admissions, "
     "free classes, or how to login/register!", None),

    (['course', 'courses', 'programs', 'program'],
     "We offer: Data Science & AI, Ethical Hacking, Python Programming, UI/UX Design, "
     "Video Editing and Graphic Designing — both online and offline. Want to see the full list?",
     'courses:course_list'),

    (['free', 'youtube', 'you tube'],
     "Yes! We provide free YouTube classes on our channel 'Learn Your Skills'. "
     "You can also find free videos for each course right here on the website.", None),

    (['fee', 'fees', 'price', 'cost', 'payment'],
     "Course fees vary by program. Please fill out our quick Enquiry form and our team will "
     "share the fee details and available offers with you.", 'courses:enquiry'),

    (['register', 'sign up', 'signup', 'admission', 'enroll', 'enrol'],
     "You can register as a student here, it only takes a minute!", 'accounts:student_register'),

    (['login', 'log in', 'sign in'],
     "Students can login here, and teachers have a separate Teacher Login page.",
     'accounts:student_login'),

    (['teacher', 'faculty', 'instructor'],
     "Our courses are taught by certified industry experts. Teachers manage their own video "
     "lessons and can mark them free or paid.", None),

    (['contact', 'phone', 'number', 'email', 'reach', 'address'],
     "The best way to reach us is through our Enquiry form — our team will contact you shortly!",
     'courses:enquiry'),

    (['offline', 'classroom', 'batch'],
     "We run structured offline professional training with small batch sizes for personalized "
     "attention, along with online programs too.", None),

    (['certificate', 'certification'],
     "Yes, all our courses include industry-recognized certification upon completion.", None),

    (['instagram', 'social'],
     "Follow us on Instagram @learn_your_skills for updates, tips and behind-the-scenes content!", None),

    (['thank', 'thanks', 'thank you'],
     "You're welcome! 😊 Happy learning with RANSOM SYNTAX!", None),

    (['bye', 'goodbye'],
     "Goodbye! Feel free to come back anytime you have a question. 🚀", None),
]

FALLBACK_REPLY = (
    "I'm not totally sure about that yet, but our team can help! "
    "Please try the Enquiry form or ask me about courses, fees, free classes, or registration."
)


def _match_reply(message):
    text = message.lower()
    for keywords, reply, url_name in RULES:
        if any(k in text for k in keywords):
            link = reverse(url_name) if url_name else None
            return reply, link
    return FALLBACK_REPLY, reverse('courses:enquiry')


@csrf_exempt
@require_POST
def ask(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = request.POST
    message = (data.get('message') or '').strip()
    if not message:
        return JsonResponse({'reply': "Please type a question and I'll do my best to help!", 'link': None})
    reply, link = _match_reply(message)
    return JsonResponse({'reply': reply, 'link': link})
