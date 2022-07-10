from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings

from users.models import Profile


# Using Django signals
@receiver(signals.post_save, sender=Profile)
def profile_updated(sender, instance, created, **kwargs):
    """Also update the user"""
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


@receiver(signals.post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    # Also delete the user
    user = instance.user
    user.delete()
    print("Profile Deleted along with User!!!")


@receiver(signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name + ' ' + user.last_name,
        )

        subject = 'Welcome to DevSearcher'
        message = 'We are glad you are here'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            ['kprocks45@gmail.com'],
            fail_silently=False,
        )

# signals.post_save.connect(profile_updated, sender=Profile)
# signals.post_delete.connect(profile_deleted, sender=Profile)
