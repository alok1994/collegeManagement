from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Add logic here to retrieve data for the Dashboard
    return render(request, 'dashboardapp/dashboard.html')
