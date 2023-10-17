from django.shortcuts import render, redirect
from .forms import CharacterCertificateForm
from django.contrib.auth.decorators import login_required
from admissionapp.models import AdmissionForm 
from django.core.paginator import Paginator
from .models import TransferCertificate
from django.utils.translation import activate



@login_required
def student_list_details_trans(request):
    # Get a list of distinct class values from the Student model
    class_choices = AdmissionForm.objects.values_list('admission_batch', flat=True).distinct()
    selected_class = request.GET.get('class_filter')  # Get the selected class from the query parameter
    # Filter fees based on the selected class (if provided)
    if selected_class:
        class_students = AdmissionForm.objects.filter(admission_batch=selected_class)
    else:
        class_students = AdmissionForm.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(class_students, 20)  # Display 10 students per page, you can adjust this number as needed

    class_students = paginator.get_page(page)


    for student in class_students:
        student_id = student.id

    return render(request, 'transfer_certificate/student_details_trans_cert.html', {'class_students': class_students, 'class_choices': class_choices, 'selected_class': selected_class,})

'''def generate_character_certificate(request, student_id):
    # Retrieve the AdmissionForm instance
    admission_form = AdmissionForm.objects.get(pk=student_id)

    if request.method == 'POST':
        form = CharacterCertificateForm(request.POST)
        if form.is_valid():
            # Save the character certificate with a link to the student
            character_certificate = form.save(commit=False)
            character_certificate.student = admission_form
            character_certificate.save()
            return redirect('view_character_certificate', student_id=student_id)
    else:
        form = CharacterCertificateForm()

    return render(request, 'character_certificate/generate_character_certificate.html', {
        'form': form,
        'admission_form': admission_form,
    })'''

def view_transfer_certificate(request, student_id):
    # Retrieve the AdmissionForm instance
    admission_form = AdmissionForm.objects.get(pk=student_id)
    transfer_certificate = TransferCertificate.objects.filter(student=admission_form).first()
    print('tC')
    return render(request, 'transfer_certificate/view_transfer_certificate.html', {
        'admission_form': admission_form,
        'transfer_certificate': transfer_certificate,
    })
