from django.urls import path
from . import views
urlpatterns = [
    path('feedback/', views.feedback, name='feedback'),
    path('contact/', views.feedback, name='contact'),
    path('team/', views.team, name='support-team'),
]
