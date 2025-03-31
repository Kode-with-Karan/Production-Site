from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from content.models import Content
from .models import Profile
from django.contrib import messages
import datetime
from notifications.models import Notification


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})


def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def dashboard(request):

    notifications = Notification.objects.filter(user=request.user).order_by("-timestamp")

    user = request.user  # ✅ This is a User instance

    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=user)
    

    # ✅ Correct: Ensure `uploaded_by` references User
    uploaded_content = Content.objects.filter(uploaded_by=profile)  
    
    profile = Profile.objects.get(user=request.user)

    total_earnings = 0
    total_views = 0
    todays_uploaded = 0
    for content in uploaded_content:
        total_earnings += content.earnings
        total_views += content.views

        if(content.uploaded_at.date() == datetime.date.today()):
            todays_uploaded += 1



    # ✅ FIXED: Filter by `user=user` instead of `profile`
    # collaborations = Collaboration.objects.filter(user=user)  

    context = {
        "total_content": uploaded_content.count(),
        # "total_collaborations": collaborations.count(),
        "uploaded_content": uploaded_content,
        # "collaborations": collaborations,
        # "total_earnings": profile.total_earnings,  
        "todays_uploaded": todays_uploaded,  
        "total_views": total_views,  
        "total_earnings": total_earnings,  
        "notifications": notifications,
        "profile": profile
        # "last_payment": profile.last_payment,  
    }

    # print(context['total_views'])

    return render(request, "users/dashboard.html", context)



# @login_required
# def collaborate(request):
#     user = request.user
#     ongoing_collaborations = Collaboration.objects.filter(user=user, status="ongoing")
#     past_collaborations = Collaboration.objects.filter(user=user, status="completed")
#     collaboration_requests = CollaborationRequest.objects.filter(user=user, status="pending")
#     available_projects = Project.objects.exclude(collaborations__user=user)  # Projects user is not part of

#     context = {
#         "ongoing_collaborations": ongoing_collaborations,
#         "past_collaborations": past_collaborations,
#         "collaboration_requests": collaboration_requests,
#         "available_projects": available_projects,
#     }
#     return render(request, "users/collaborate.html", context)

# @login_required
# def apply_collaboration(request):
#     if request.method == "POST":
#         project_id = request.POST.get("project")
#         role = request.POST.get("role")
#         project = get_object_or_404(Project, id=project_id)
#         CollaborationRequest.objects.create(user=request.user, project=project, requested_role=role, status="pending")
#         messages.success(request, "Collaboration request sent successfully!")
#         return redirect("collaborate")
#     return redirect("collaborate")

# @login_required
# def accept_collaboration(request, request_id):
#     collab_request = get_object_or_404(CollaborationRequest, id=request_id, status="pending")
#     collab_request.status = "accepted"
#     collab_request.save()
#     Collaboration.objects.create(users=[collab_request.user], project=collab_request.project, role=collab_request.requested_role, status="ongoing")
#     messages.success(request, "Collaboration request accepted!")
#     return redirect("collaborate")

# @login_required
# def reject_collaboration(request, request_id):
#     collab_request = get_object_or_404(CollaborationRequest, id=request_id, status="pending")
#     collab_request.status = "rejected"
#     collab_request.save()
#     messages.error(request, "Collaboration request rejected.")
#     return redirect("collaborate")