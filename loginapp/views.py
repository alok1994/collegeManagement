from django.shortcuts import render,redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib import messages


def logout_view(request):
    logout(request)
    return render(request, 'loginapp/logout.html')

def CustomLoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

    return render(request, 'loginapp/login.html')

