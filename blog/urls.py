from django.urls import path
from .views import (
    blog_list, blog_detail, blog_create, blog_update, blog_delete, blog_share
)

urlpatterns = [
    # Blog-related URLs
    path('', blog_list, name='blog_list'),  # List all blogs
    path('create/', blog_create, name='blog_create'),
    path('<slug:slug>/', blog_detail, name='blog_detail'),  # Blog detail view
    path('<slug:slug>/update/', blog_update, name='blog_update'),  # Update blog
    path('<slug:slug>/delete/', blog_delete, name='blog_delete'),  # Delete blog
    
    # Blog Analytics & Sharing
    path('<slug:slug>/share/', blog_share, name='blog_share'),  # Track shares
]
