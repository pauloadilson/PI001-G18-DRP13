from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterModelForm

from django.views.generic import CreateView

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

class RegisterUserView(CreateView):
    model = User
    form_class = RegisterModelForm
    template_name = "registration/register.html"
    page_title = "Registrando Usuário"
    form_title = "Registrando Usuário"
    success_url = reverse_lazy("index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form_title"] = self.form_title
        return context
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            # Adicione o usuário aos grupos selecionados
            user.groups.set(form.cleaned_data['groups'])
            user.save()
            return redirect('index')
        return render(request, self.template_name, {'form': form})