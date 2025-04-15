from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("login", views.login_view, name="login"),
    path("change_pass", views.change_password, name="change_pass"),
    path("my_account", views.user_profile, name="user_profile"),
    path("logout", views.logout_view, name="logout"),
]