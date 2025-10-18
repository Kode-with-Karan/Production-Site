from django.urls import path, include
from .views import * 
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Password reset request
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/password_reset_subject.txt'
        ),
        name='password_reset'
    ),

    # Password reset done page
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Password reset confirm (link in email)
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # Password reset complete
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),


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
