# """
# URL configuration for config project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path, include
# # Import the home view
# from config.views import home  
# from django.conf.urls.static import static
# from django.conf import settings
# from django.urls import path
# from apps.users.views import signup_view
# from django.shortcuts import render


# def home(request):
#     return render(request, "home.html")

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path("", home, name='home'),  # Define the homepage
#     path('movies/', include('apps.movies.urls')),  # Movie-related URLs
#     path('events/', include('apps.events.urls')),  # "Events" has a placeholder
#     path("bookings/", include("apps.bookings.urls")),  # Booking URLs added here
#     path('accounts/', include('django.contrib.auth.urls')),  # Adds Django Built-in login/logout/register views
#     path("users/", include("apps.users.urls")),
#     path("signup/", signup_view, name="signup"),
#     path("payments/", include("apps.payments.urls")),
#      #path("notifications/", include("apps.notifications.urls")),  # Register notifications app

# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from config.views import home  
from django.conf.urls.static import static
from django.conf import settings
from apps.users.views import signup_view
from django.shortcuts import render
def terms_view(request):
    return render(request, "terms.html")

def privacy_view(request):
    return render(request, "privacy.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name='home'),  # uses home from views.py
    path('movies/', include('apps.movies.urls')),  
    path('events/', include('apps.events.urls')),  
    path("bookings/", include("apps.bookings.urls")),  
    path('accounts/', include('django.contrib.auth.urls')),  
    path("users/", include("apps.users.urls")),
    path("signup/", signup_view, name="signup"),
    path("payments/", include("apps.payments.urls")),
    path("terms/", terms_view, name="terms"),
    path("privacy/", privacy_view, name="privacy"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
