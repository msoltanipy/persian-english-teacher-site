from django.conf import settings
from .models import TeacherProfile


def site_profile(request):
    profile = TeacherProfile.objects.first()
    telegram_username = (
        profile.clean_telegram_username if profile else settings.TELEGRAM_USERNAME
    )
    return {
        "teacher_profile": profile,
        "telegram_username": telegram_username,
    }
