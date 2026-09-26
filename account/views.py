from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from account.forms import Login_form, edit_user_form,Register_form,edit_profile_form
from django.views.generic.base import View

from account.models import Profile
from chronicle.models import Post


def login_user(request):
    if request.user.is_authenticated == True:
        return redirect('home:home')
    if request.method == "POST":
        form = Login_form(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['username'])
            login(request, user)
            return redirect('home:home')
    else:
        form = Login_form()
    return render(request, "account/login.html", context={'form': form})


def logout_user(request):
    logout(request)
    return redirect('home:home')


def register_user(request):
    form = Register_form()
    if request.method == "POST":
        form = Register_form(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username,email=email,password=password)
            return redirect('account:login')
    return render(request, "account/register.html", context={'form': form})


def edit_user(request):
    user = request.user

    profile, created = Profile.objects.get_or_create(user=user)

    user_form = edit_user_form(instance=user)
    profile_form = edit_profile_form(instance=profile)

    if request.method == "POST":
        user_form = edit_user_form(
            instance=user,
            data=request.POST
        )

        profile_form = edit_profile_form(
            instance=profile,
            data=request.POST,
            files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home:home')

    return render(
        request,
        "account/edit.html",
        context={
            'user_form': user_form,
            'profile_form': profile_form,
        }
)


class Listview(View):
    template_name = None
    queryset = None

    def get(self, request):
        return render(request, self.template_name, {'': self.queryset})
