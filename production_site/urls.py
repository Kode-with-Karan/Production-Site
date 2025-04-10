"""
URL configuration for production_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from content.views import custom_404_view

handler404 = "content.views.custom_404_view" 


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('', include('content.urls')),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('payments/', include('payments.urls')),
    path('notifications/', include('notifications.urls')),  # ✅ Notifications URLs
    path('support/', include('support.urls')),  # ✅ Support URLs
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('investor/', TemplateView.as_view(template_name="pages/investor.html"), name='investor'),
    path('talent/', TemplateView.as_view(template_name="pages/talent.html"), name='talent'),
    path('filmmaker/', TemplateView.as_view(template_name="pages/filmmaker.html"), name='filmmaker'),
    path('terms/', TemplateView.as_view(template_name="pages/terms.html"), name='terms'),
    path('team/', TemplateView.as_view(template_name="pages/team.html"), name='team'),
    path('faq/', TemplateView.as_view(template_name="pages/faq.html"), name='faq'),
    path('privacy/', TemplateView.as_view(template_name="pages/privacy.html"), name='privacy'),
    path('about/', TemplateView.as_view(template_name="pages/about.html"), name='about'),
    path('pricing/', TemplateView.as_view(template_name="pages/pricing.html"), name='pricing'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)