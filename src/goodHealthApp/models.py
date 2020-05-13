from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from .util import modelUtil


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    avatar = models.FileField(upload_to=modelUtil.get_upload_path)

    def __str__(self):  # __unicode__ for Python 2
        return self.first_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def get_upload_path(instance, filename):
    year = now().year
    month = now().month
    day = now().day
    return 'uploads/{0}/{1}/{2}/'.format(year, month, day) + filename


class UserPost(models.Model):
    """
    UserPost Model for each post created by a user.

    It can be an anonymous post without extra information. Only one media
    file is required when creating a post and the time is stamped at the
    point of creating the record.
    """
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True,
                             blank=True)
    anonymous = models.BooleanField(default=True)
    media1 = models.FileField(upload_to=get_upload_path)
    media2 = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    media3 = models.FileField(upload_to=get_upload_path, null=True, blank=True)
    location = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra = models.TextField(blank=True)

    class Meta:
        """
        UserPost Meta class.
        """
        ordering = ['-created_at']

    def __str__(self):
        """
        Converts  UserPost object to a string.

        :returns: the users name and time of post
        :rtype: string
        """
        if self.user == None:
            user = "user_not_found"
        else:
            user = str(self.user)
        return user + " - " + str(self.created_at)


# ADEMOLA - EmergencyLine Model
class EmergencyLine(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    # property
    def __str__(self):
        return self.name
