from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)   
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'sign_up.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password. Please check your input.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})
    



        