from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", default="default.jpg", blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    stripe_account_id = models.CharField(max_length=255, blank=True, null=True)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    last_payment = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
