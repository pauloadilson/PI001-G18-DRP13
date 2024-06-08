from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

def redirect_if_logged_in(func):
    def inner_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return func(request, *args, **kwargs)
    return inner_func

# Login Page
@redirect_if_logged_in
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
