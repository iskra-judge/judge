from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as views

from judge.judge_auth.forms import SignUpForm, SignInForm


class SignUpView(views.CreateView):
    form_class = SignUpForm
    template_name = 'auth/sign-up.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return valid


class SignInView(auth_views.LoginView):
    template_name = 'auth/sign-in.html'
    form_class = SignInForm


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')
