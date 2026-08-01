# Generated for Ransom Syntax course access control

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_course_classroom_code_course_classroom_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(
                blank=True,
                help_text='Teacher(s) who own/manage this course. Set by Admin.',
                related_name='teaching_courses',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
