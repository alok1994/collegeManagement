from django.shortcuts import render, redirect, get_object_or_404
from .models import Fee
from .forms import FeeForm
from admissionapp.models import AdmissionForm  # Import the Student model
from django.db.models import Max
from datetime import datetime
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from num2words import num2words

@login_required
def fee_detail(request):
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

    return render(request, 'fee_management/fee_detail.html', {'class_students': class_students, 'class_choices': class_choices, 'selected_class': selected_class,})

@login_required
def fee_submission(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)

    if request.method == 'POST':
        fee_form = FeeForm(request.POST)
        if fee_form.is_valid():
            # Create a new Fee instance
            fee = fee_form.save(commit=False)
            
            # Set the student for the fee
            fee.student = student

            # Generate a receipt number
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            random_part = get_random_string(length=6, allowed_chars='1234567890')
            fee.receipt_number = f"R{timestamp}{random_part}"

            # Handle fields that might be None
            fee.registration_fee = fee.registration_fee or 0
            fee.tuition_fee = fee.tuition_fee or 0
            fee.exam_fee = fee.exam_fee or 0
            fee.sports_fee = fee.sports_fee or 0
            fee.miscellaneous_fee = fee.miscellaneous_fee or 0

            # Calculate the Total Amount
            total_paid_amount = (
                fee.registration_fee + fee.tuition_fee + fee.exam_fee +
                fee.sports_fee + fee.miscellaneous_fee
            )
            fee.total_paid_amount = total_paid_amount

            # Convert the Total Amount to Indian currency in words
            total_amount_in_words = num2words(total_paid_amount, lang='en_IN')
            fee.total_amount_in_words = total_amount_in_words

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

'''@login_required
def generate_receipt(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id)
    student = fee.student

    context = {
        'student': student,
        'fee': fee,
    }

    return render(request, 'fee_management/receipt.html', context)'''

