from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, CommentForm
from .models import Blog, BlogAnalytics, Category
from django.db.models import F
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Count

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    
    # Increment blog views
    blog.views = F('views') + 1
    blog.save(update_fields=['views'])

    # Update analytics views
    analytics, created = BlogAnalytics.objects.get_or_create(blog=blog)
    analytics.views = F('views') + 1
    analytics.save(update_fields=['views'])
    # Fetch approved comments
    comments = blog.comments.all()
    # comments = blog.comments.filter(approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment is awaiting approval.")
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = CommentForm()

    related_blogs = Blog.objects.filter(
        Q(category=blog.category) | Q(tags__in=blog.tags.all())
    ).exclude(id=blog.id).distinct()[:5]  # Limit to 5 related posts

    categories = Category.objects.annotate(blog_count=Count('blog')).order_by('-blog_count')

    return render(request, 'blog/blog_detail.html', {'blog': blog, 'comments': comments, 'form': form, 'related_blogs': related_blogs, 'categories': categories,})


def blog_list(request):
    blogs = Blog.objects.filter(status='published').order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            form.save_m2m()
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = BlogForm()
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def blog_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def blog_delete(request, slug):
    blog = get_object_or_404(Blog, slug=slug, author=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog/blog_confirm_delete.html', {'blog': blog})

def blog_share(request, slug):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, slug=slug, status='published')
        analytics, created = BlogAnalytics.objects.get_or_create(blog=blog)
        analytics.shares = F('shares') + 1
        analytics.save(update_fields=['shares'])
        return JsonResponse({'message': 'Share count updated'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)