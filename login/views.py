from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


# Login Page
def user_login(request):
    page_title = "Login..."
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
    return render(request, "registration/login.html", {"form": form, "page_title": page_title})


# Logout Page
def user_logout(request):
    logout(request)
    return redirect("index")
