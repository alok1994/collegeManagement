from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chartjs.views.lines import BaseLineChartView
from admissionapp.models import AdmissionForm
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.models import User



@login_required
def dashboard(request):
    # Add logic here to retrieve data for the Dashboard
    total_users = User.objects.all().count()

    context = {
        'total_users': total_users,
    }
    return render(request, 'dashboardapp/dashboard.html', context)

def get_user_count(request):
    # Retrieve the user count from the User model
    user_count = User.objects.count()
    print(user_count)
    # Create a JSON response with the user count
    response_data = {'total_users': user_count}
    return JsonResponse(response_data)