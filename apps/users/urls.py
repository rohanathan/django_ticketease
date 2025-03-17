from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, dashboard, edit_profile, login_view

urlpatterns = [
    path("register/", register, name="register"),
    path("dashboard/", dashboard, name="dashboard"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),  #  Added logout
]
