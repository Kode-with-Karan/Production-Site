from django.db import models
from users.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


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
        ('short_series', 'Short Series'),
        ('drama', 'Drama'),
        ('shorts', 'Shorts'),
        ('web_shorts', 'Web Shorts'),
        ('feature_series', 'Feature Series'),
        ('stand_up', 'Stand Up Comedy'),
        ('Other', 'Other'),
        

    ]

    REGION_TYPE = [
        ('English', 'English'),
        ('Indian', 'Indian'),
        ('French', 'French'),
        ('Russian', 'Russian'),
        ('German', 'German'),
        ('Spanish', 'Spanish'),
        ('Japanese', 'Japanese'),
        ('Italian', 'Italian'),
        ('Other', 'Other'),
    ]

    GENRE_TYPE = [
        ('Comedy', 'Comedy'),
        ('Action', 'Action'),
        ('Romantic', 'Romantic'),
        ('Thriller', 'Thriller'),
        ('Horror', 'Horror'),
        ('Magic', 'Magic'),
        ('Poem', 'Poem'),
        ('History', 'History'),
        ('Epic', 'Epic'),
        ('Health', 'Health'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ( "Other" ,"Other"),
    ]

    LANGUAGE_TYPE = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('French', 'French'),
        ('Russian', 'Russian'),
        ('German', 'German'),
        ('Spanish', 'Spanish'),
        ('Japanese', 'Japanese'),
        ('Italian', 'Italian'),
        ('Regional_language', 'Regional_language'),
        ( "Other" ,"Other"),
    ]

    AGE_RATING_CHOICES = [
        ('7+', '7+'),
        ('10+', '10+'),
        ('13+', '13+'),
        ('16+', '16+'),
        ('18+', '18+'),
        ('Below 18', 'Below 18'),
    ]
    
    
    title = models.CharField(max_length=200)
    country = models.CharField(max_length=50, choices=REGION_TYPE)
    duration = models.CharField(max_length=200,default="Not Mentioned")
    genre = models.CharField(max_length=50, choices=GENRE_TYPE)
    language = models.CharField(max_length=50, choices=LANGUAGE_TYPE)
    age_rating = models.CharField(max_length=10, choices=AGE_RATING_CHOICES, default='7+')
    description = models.TextField()
    cast = models.TextField(default="Not Mentioned")
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='content_files/')

    is_premium = models.BooleanField(default=False)
    preview_duration = models.PositiveIntegerField(default=20) 
    
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
        ('short_series', 'Short Series'),
        ('drama', 'Drama'),
        ('shorts', 'Shorts'),
        ('web_shorts', 'Web Shorts'),
        ('feature_series', 'Feature Series'),

    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collaborations")
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    idea_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
 

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
    

class Ad(models.Model):
    category = models.CharField(max_length=100)
    video_url = models.FileField(upload_to='ads/')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.category})"

class AdView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ForeignKey('content.Content', on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    watched_full = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} watched Ad {self.ad.title} (Full: {self.watched_full})"
    
class Contest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.TextField()
    country = models.TextField()
    genre = models.TextField()
    description = models.TextField()
    file_url = models.URLField()
    

    def __str__(self):
        return f"{self.user} from {self.country}"
