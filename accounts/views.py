from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import logout, login

from . import forms


class SignUp(CreateView):
    form_class = forms.CustomUserCreationForm
    # Only reverse(goes) to the page only after the user has hit submit
    success_url = reverse_lazy('accounts:login')
    # template_name = ''


@login_required
def logged_out(request):
    logout(request)
    # return render(request, 'accounts/logged_out.html')
    return redirect('mapp:home')


def logged_in(request):
    login(request)
    return redirect('mapp:home')
