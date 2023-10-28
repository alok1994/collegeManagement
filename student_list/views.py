from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from admissionapp.models import AdmissionForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import AdmissionYearFilterForm, AdmissionClassFilterForm
from .forms import StudentUpdateForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect



@login_required
def student_list(request):
    students = AdmissionForm.objects.all()

    # Apply filters if provided in the GET request
    year_filter_form = AdmissionYearFilterForm(request.POST)
    if year_filter_form.is_valid():
        admission_year = year_filter_form.cleaned_data.get('admission_year')    
        if admission_year:
            students = students.filter(admission_date__year=admission_year)

    class_filter_form = AdmissionClassFilterForm(request.POST)
    if class_filter_form.is_valid():
        admission_batch = class_filter_form.cleaned_data.get('admission_batch')
        if admission_batch:
            students = students.filter(admission_batch__icontains=admission_batch)

    # Paginate the student list
    page = request.GET.get('page')
    paginator = Paginator(students, 20)  # Display 10 students per page, you can adjust this number as needed

    students = paginator.get_page(page)

    context = {
        'students': students,
        'year_filter_form': year_filter_form,
        'class_filter_form': class_filter_form,
    }

    return render(request, 'student_list/student_list.html', context)

@login_required
def student_details(request, student_id):
    student = get_object_or_404(AdmissionForm, pk=student_id)
    return render(request, 'student_list/student_details.html', {'student': student})

@login_required
def update_student(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('student_list')  # Redirect back to the student list page
    else:
        form = StudentUpdateForm(instance=student)

    context = {
        'student': student,
        'form': form,
    }

    return render(request, 'student_list/update_student.html', context)

@login_required
def first_year(request):
    first_year_students = AdmissionForm.objects.filter(admission_batch='1')
   
    # Apply filters if provided in the GET request
    year_filter_form = AdmissionYearFilterForm(request.GET)
    if year_filter_form.is_valid():
        admission_year = year_filter_form.cleaned_data.get('admission_year')
        if admission_year:
            first_year_students = first_year_students.filter(admission_date__year=admission_year)

    # Paginate the class 6 student list
    page = request.GET.get('page')
    paginator = Paginator(first_year_students, 20)  # Display 10 students per page, you can adjust this number as needed

    first_year_students = paginator.get_page(page)

    context = {
        'first_year_students': first_year_students,
        'year_filter_form': year_filter_form,
    }

    return render(request, 'student_list/first_year.html', context)


@login_required
def second_year(request):
    second_year_students = AdmissionForm.objects.filter(admission_batch='2')
    
    # Apply filters if provided in the GET request
    year_filter_form = AdmissionYearFilterForm(request.GET)
    if year_filter_form.is_valid():
        admission_year = year_filter_form.cleaned_data.get('admission_year')
        if admission_year:
            second_year_students = second_year_students.filter(admission_date__year=admission_year)

    # Paginate the class 6 student list
    page = request.GET.get('page')
    paginator = Paginator(second_year_students, 20)  # Display 10 students per page, you can adjust this number as needed

    second_year_students = paginator.get_page(page)

    context = {
        'second_year_students': second_year_students,
        'year_filter_form': year_filter_form,
    }

    return render(request, 'student_list/second_year.html', context)


@login_required
def third_year(request):
    third_year_students = AdmissionForm.objects.filter(admission_batch='3')
    
    # Apply filters if provided in the GET request
    year_filter_form = AdmissionYearFilterForm(request.GET)
    if year_filter_form.is_valid():
        admission_year = year_filter_form.cleaned_data.get('admission_year')
        if admission_year:
            third_year_students = third_year_students.filter(admission_date__year=admission_year)

    # Paginate the class 6 student list
    page = request.GET.get('page')
    paginator = Paginator(third_year_students, 20)  # Display 10 students per page, you can adjust this number as needed

    third_year_students = paginator.get_page(page)

    context = {
        'third_year_students': third_year_students,
        'year_filter_form': year_filter_form,
    }

    return render(request, 'student_list/third_year.html', context)

@login_required
def update_student_first_year(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('first_year')  # Redirect back to the class 6 page
    else:
        form = StudentUpdateForm(instance=student)

    context = {
        'student': student,
        'form': form,
    }

    return render(request, 'student_list/update_student.html', context)

@login_required
def update_student_second_year(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('second_year')  # Redirect back to the class 6 page
    else:
        form = StudentUpdateForm(instance=student)

    context = {
        'student': student,
        'form': form,
    }

    return render(request, 'student_list/update_student.html', context)

@login_required
def update_student_third_year(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('third_year')  # Redirect back to the class 6 page
    else:
        form = StudentUpdateForm(instance=student)

    context = {
        'student': student,
        'form': form,
    }

    return render(request, 'student_list/update_student.html', context)


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)
    student.delete()
    messages.success(request, 'Student deleted successfully.')
    return HttpResponseRedirect(reverse('student_list'))  
