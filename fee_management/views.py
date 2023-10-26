from django.shortcuts import render, redirect, get_object_or_404
from .models import Fee
from .forms import FeeForm
from admissionapp.models import AdmissionForm  
from django.db.models import Max
from datetime import datetime
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from num2words import num2words
from fee_structure.models import Semester 
from django.db.models import Sum

@login_required
def fee_detail(request):
    # Get a list of distinct semester values from the Student model
    semester_choices = AdmissionForm.objects.values_list('current_semester', flat=True).distinct()

    # Get the selected class from the query parameter
    
    selected_class = request.GET.get('class_filter') 

    # Filter fees based on the selected class (if provided)
    if selected_class:
        class_students = AdmissionForm.objects.filter(current_semester=selected_class)
    else:
        class_students = AdmissionForm.objects.all()

    page = request.GET.get('page')
    # Display 10 students per page, you can adjust this number as needed
    paginator = Paginator(class_students, 20)  

    class_students = paginator.get_page(page)


    for student in class_students:
        student_id = student.id

    return render(request, 'fee_management/fee_detail.html', {'class_students': class_students, 'semester_choices': semester_choices, 'selected_class': selected_class,})


@login_required
def fee_submission(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)

    if request.method == 'POST':
        fee_form = FeeForm(request.POST)
        if fee_form.is_valid():
            fee = fee_form.save(commit=False)
            fee.student = student

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_part = get_random_string(length=6, allowed_chars='1234567890')
            fee.receipt_number = f"R{timestamp}{random_part}"

            fee.registration_fee = fee.registration_fee or 0
            fee.tuition_fee = fee.tuition_fee or 0
            fee.exam_fee = fee.exam_fee or 0
            fee.sports_fee = fee.sports_fee or 0
            fee.miscellaneous_fee = fee.miscellaneous_fee or 0
            fee.late_fee = fee.late_fee or 0
            fee.discount_fee = fee.discount_fee or 0

            total_paid_amount = (
                fee.registration_fee + fee.tuition_fee + fee.exam_fee +
                fee.sports_fee + fee.miscellaneous_fee - fee.discount_fee + fee.late_fee
            )
            fee.total_paid_amount = total_paid_amount

            fee.semester = student.current_semester

            # Query the database to get the fee history for the selected student
            fee_history = Fee.objects.filter(student=student).order_by('-payment_date')

            # Get the student's current semester from the AdmissionForm
            current_semester = student.current_semester

            try:
                semester_fee = Semester.objects.get(semester_number=student.current_semester)
                total_semester_fee = semester_fee.semester_total
                fee.total_semester_fee = total_semester_fee
            except Semester.DoesNotExist:
                total_semester_fee = 0

            # Calculate the total paid amount for the student
            total_paid_amount_history = {}  # Dictionary to store total paid amounts per semester

            # Iterate through fee history to calculate total paid amounts per semester
            for history_entry in fee_history:
                semester_paid = history_entry.semester
                if semester_paid not in total_paid_amount_history:
                    total_paid_amount_history[semester_paid] = 0
                total_paid_amount_history[semester_paid] += history_entry.total_paid_amount

            # Handle the case where current semester doesn't have a paid amount entry
            if current_semester not in total_paid_amount_history:
                total_paid_amount_history[current_semester] = 0

            # Calculate the remaining amount for the current semester
            remaining_amount = total_semester_fee - total_paid_amount - total_paid_amount_history[current_semester]
            fee.remaining_amount = remaining_amount

            fee.save()

            return redirect('generate_receipt', fee_id=fee.id)
        else:
            print(fee_form.errors)

    else:
        fee_form = FeeForm() 

    return render(request, 'fee_management/fee_submission.html', {'fee_form': fee_form, 'student': student})



@login_required
def generate_receipt(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id)
    student = fee.student

    context = {
        'student': student,
        'fee': fee
    }

    return render(request, 'fee_management/receipt.html', context)

@login_required
def fee_history(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)  # Get the student by ID

    # Query the database to get the fee history for the selected student
    fee_history = Fee.objects.filter(student=student).order_by('-payment_date')

    return render(request, 'fee_management/fee_history.html', {'student': student, 'fee_history': fee_history})




