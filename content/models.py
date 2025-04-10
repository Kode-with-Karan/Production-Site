from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone


class Content(models.Model):
    CONTENT_TYPES = [
        ('short_film', 'Short Film'),
        ('podcast', 'Podcast'),
        ('documentary', 'Documentary'),
        ('entertainment', 'Entertainment Project'),
        ('music', 'Music'),
        ('education', 'Education'),
        ('interviews', 'Interviews'),
        ('animation', 'Animation'),
        ('web_series', 'Web Series'),
    ]
    
    title = models.CharField(max_length=200)
    country = models.CharField(max_length=200,default="Not Mentioned")
    duration = models.CharField(max_length=200,default="Not Mentioned")
    genre = models.CharField(max_length=200,default="Not Mentioned")
    language = models.CharField(max_length=200,default="Not Mentioned")
    age_rating = models.IntegerField(default="0")
    description = models.TextField()
    cast = models.TextField(default="Not Mentioned")
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='content_files/')

    is_premium = models.BooleanField(default=False)
    preview_duration = models.PositiveIntegerField(default=60) 
    
    thumbnail = models.ImageField(upload_to='content_thumbnails/', blank=True)
    uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contents")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_rating = models.FloatField(default=0.0)
    total_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('user', 'content')  # Ensures a user can rate content only once

class Collaborate(models.Model):
    CONTENT_TYPES = [
        ('short_film', 'Short Film'),
        ('podcast', 'Podcast'),
        ('documentary', 'Documentary'),
        ('entertainment', 'Entertainment Project'),
        ('music', 'Music'),
        ('education', 'Education'),
        ('interviews', 'Interviews'),
        ('animation', 'Animation'),
        ('web_series', 'Web Series'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collaborations")
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    idea_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
#     file = models.FileField(upload_to='content_files/')
#     thumbnail = models.ImageField(upload_to='content_thumbnails/', blank=True)
#     # uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contents")
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     views = models.PositiveIntegerField(default=0)
#     earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    

class PromotedContent(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey("content.Content", on_delete=models.CASCADE)
    promotion_start = models.DateTimeField(default=timezone.now)
    promotion_end = models.DateTimeField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.promotion_end < timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.content.title} promoted by {self.creator.username}"
    
# class Project(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class Collaboration(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="collaborations")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collaborations")
#     role = models.CharField(max_length=255)
#     status = models.CharField(max_length=20, choices=[("ongoing", "Ongoing"), ("completed", "Completed")], default="ongoing")

#     def __str__(self):
#         return f"{self.user.username} - {self.project.name} ({self.role})"

# class CollaborationRequest(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="collab_requests")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collab_requests")
#     requested_role = models.CharField(max_length=255)
#     status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")], default="pending")

#     def __str__(self):
#         return f"{self.user.username} requested {self.requested_role} in {self.project.name}"