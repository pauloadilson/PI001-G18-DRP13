from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


# Home Page
@login_required(login_url="login")
def home(request):
    return render(request, "login/home.html")


# Login Page
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("../")

    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


# Logout Page
def user_logout(request):
    logout(request)
    return redirect("index")
