from django.views import View
from django.views.generic import CreateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import RegisterForm
from .forms import LoginForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('home')


class LoginView(FormView):
    template_name = "auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.login(self.request)
        return super().form_valid(form)


class Logout(View):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            logout(request)
            return redirect('home')
