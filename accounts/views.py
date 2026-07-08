# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout

def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = RegisterForm()

    context = {
        'form': form
    }

    return render(
        request,
        'accounts/register.html',
        context
    )

def user_login(request):
    if request.user.is_authenticated:
        return redirect('student_list')
    
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user) #Django phir user ka session create kar deta hai.

            return redirect('student_list')

    else:

        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(
        request,
        'accounts/login.html',
        context
    )

def user_logout(request):

    logout(request)

    return redirect('login')