from django.shortcuts import render, redirect
from .models import AdmissionForm
from .forms import AdmissionFormForm
from django.http import HttpResponse
from django.http import JsonResponse

def admission_form(request):
    if request.method == 'POST':
        form = AdmissionFormForm(request.POST, request.FILES)
       
        if form.is_valid():
            #photo = request.FILES['photo']
            #print(f'Uploaded file name: {photo.name}')
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                print(f'Uploaded file name: {photo.name}')
            else:
                # Handle the case where 'photo' is not attached
                print("No photo attached in the form.")
            admission = form.save()
            # You can redirect to a success page or display a success message here
            return redirect('student_details', student_id=admission.id)
        else:
            # If there are form validation errors, you can print them to see what's wrong
            print(form.errors)
    else:
        form = AdmissionFormForm()
    
    context = {
        'form': form,
    }
    return render(request, 'admissionapp/admission_form.html', context)

def admission_success(request):
    # You can customize this view to display a success message or redirect to another page
    return render(request, 'admissionapp/admission_success.html')


def student_data_api(request):
    # Query the database to retrieve student data
    students = AdmissionForm.objects.all()

    student_data = [
        {
            'first_name': student.first_name,
            'middle_name': student.middle_name,
            'last_name': student.last_name,
            'admission_batch': student.admission_batch,
        }
        for student in students
    ]

    # Return the JSON response
    return JsonResponse(student_data, safe=False)