from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class confirm_email(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} UserProfile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         confirm_email.objects.create(user=instance)
#         instance.confirm_email.save()


class UserProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    user_confirm = models.BooleanField(
        default=False,
    )

    address = models.CharField(
        max_length=100,
        null=True,
    )

    parish = models.CharField(
        max_length=100,
        null=True,
    )
    # trnnumber = models.CharField(max_length=100, null=True)
    mobilenumber = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user.username} UserProfile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)