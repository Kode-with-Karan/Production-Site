from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Blog Model
class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    
    banner_image = models.ImageField(upload_to='blog_banners/', blank=False, null=False)  # Required
    main_image = models.ImageField(upload_to='blog_main/', blank=False, null=False)  # Required
    optional_image1 = models.ImageField(upload_to='blog_optional/', blank=True, null=True)
    optional_image2 = models.ImageField(upload_to='blog_optional/', blank=True, null=True)
    optional_image3 = models.ImageField(upload_to='blog_optional/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Comment Model
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'

# Blog Analytics Model
class BlogAnalytics(models.Model):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE, related_name='analytics')
    views = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'Analytics for {self.blog.title}'
