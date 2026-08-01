from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import TeacherProfile
from courses.models import Course, Video

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with a demo teacher, courses and videos so you can explore the site immediately."

    def handle(self, *args, **options):
        # Demo teacher
        if not User.objects.filter(username='demo_teacher').exists():
            teacher = User.objects.create_user(
                username='demo_teacher', password='TeachDemo123!',
                email='teacher@ransomsyntax.test', first_name='Aisha', last_name='Rahman',
                role=User.ROLE_TEACHER,
            )
            TeacherProfile.objects.create(user=teacher, subject='Data Science & AI', bio='Lead Data Science instructor.')
            self.stdout.write(self.style.SUCCESS("Created demo teacher -> username: demo_teacher / password: TeachDemo123!"))
        else:
            teacher = User.objects.get(username='demo_teacher')

        # The only 5 courses that should exist on this site.
        demo_courses = [
            ('Data Science and AI', 'Master Python, statistics, ML and AI with real projects.',
             'https://classroom.google.com/c/ODcxMjU1NjkwNjIw?cjc=f2uabqvl'),
            ('AI Assisted Data Science', 'Apply AI tooling to accelerate real-world data science workflows.',
             'https://classroom.google.com/c/ODcxMjU3NDkzNDk2?cjc=rxgadlsu'),
            ('Python Programming', 'From basics to advanced Python for real-world apps.',
             'https://classroom.google.com/c/ODU1NzA5NTI2NTI0?cjc=x7k5ikz3'),
            ('Python Full Stack (Django)', 'Build and ship full-stack web apps with Django.',
             'https://classroom.google.com/c/ODU1NzA5NjY5MzY0?cjc=xnkmn6qk'),
            ('Ethical Hacking', 'Learn penetration testing and cybersecurity fundamentals.',
             'https://classroom.google.com/c/ODU1NzA4NzU2NzEz?cjc=q2ncxbil'),
        ]
        allowed_titles = [c[0] for c in demo_courses]

        # Remove any course that is not one of the 5 required courses.
        removed = Course.objects.exclude(title__in=allowed_titles)
        removed_count = removed.count()
        removed.delete()
        if removed_count:
            self.stdout.write(self.style.WARNING(f"Removed {removed_count} course(s) not in the required list."))

        for title, desc, classroom_url in demo_courses:
            course, created = Course.objects.get_or_create(
                title=title,
                defaults={
                    'short_description': desc,
                    'description': desc,
                    'mode': Course.MODE_BOTH,
                    'classroom_url': classroom_url,
                    'is_active': True,
                },
            )
            if not created:
                # Keep existing course but make sure the classroom link/status are correct.
                course.classroom_url = classroom_url
                course.is_active = True
                course.save(update_fields=['classroom_url', 'is_active'])

            if created:
                Video.objects.create(course=course, uploaded_by=teacher, title=f"{title} - Introduction",
                                      description="A free introductory lesson.", is_free=True, order=1)
                Video.objects.create(course=course, uploaded_by=teacher, title=f"{title} - Advanced Concepts",
                                      description="Premium lesson - unlocked individually by your tutor.",
                                      is_free=False, order=2)

        self.stdout.write(self.style.SUCCESS("The 5 required courses are now set up! Visit /courses/ to explore."))
