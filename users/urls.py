from django.urls import path, include
from .views import * 
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path("dashboard/", dashboard, name="dashboard"),
    # path("collaborate/", collaborate, name="collaborate"),
    # path("apply_collaboration/", apply_collaboration, name="apply_collaboration"),
    # path("accept_collaboration/<int:request_id>/", accept_collaboration, name="accept_collaboration"),
    # path("reject_collaboration/<int:request_id>/", reject_collaboration, name="reject_collaboration"),
    path('change-password/', PasswordChangeView.as_view(template_name='users/change_password.html'), name='change_password'),
    # path('social/', include('allauth.socialaccount.urls')),
    path('', include('allauth.socialaccount.urls')),
]
