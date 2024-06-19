from django.urls import path
from . import views
from login.views import RegisterUserView

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", RegisterUserView.as_view(), name="register"),
]