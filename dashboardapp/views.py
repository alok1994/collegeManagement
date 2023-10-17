from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chartjs.views.lines import BaseLineChartView
from admissionapp.models import AdmissionForm
from django.db.models import Count
from django.http import JsonResponse


@login_required
def dashboard(request):
    # Add logic here to retrieve data for the Dashboard
    return render(request, 'dashboardapp/dashboard.html')
