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
from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse
import threading
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from loginapp.decorators import allowed_users
from django.utils import timezone
from django.http import JsonResponse
from django.core.serializers import serialize
from decimal import Decimal
import json
from django.db.models.functions import TruncMonth
from django.db.models.functions import TruncYear
from datetime import timedelta
from django.db import transaction


Tfrom  = '+13348304110'

@login_required
@allowed_users(allowed_roles=['admin'])
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
    paginator = Paginator(class_students, 24)  

    class_students = paginator.get_page(page)

    for student in class_students:
        student_id = student.id

    return render(request, 'fee_management/fee_detail.html', {'class_students': class_students, 'semester_choices': semester_choices, 'selected_class': selected_class,})


@login_required
@allowed_users(allowed_roles=['admin'])
def fee_submission(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)

    def send_message_background(total_paid_amount, current_semester, remaining_amount):
        # Construct the message
        message = f"प्रिय छात्र/छात्रा {student.first_name}, यह संदेश चन्द्रिका प्रसाद महाविद्यालय से है | आपने {total_paid_amount} रुपये Semester {current_semester } के लिए भुगतान किया है. {remaining_amount } रुपये शेष है |. कृपया जल्द से जल्द भुगतान करें।"

        # Use Twilio to send the message
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Sanitize the phone number (remove non-numeric characters)
        to_number = ''.join(filter(str.isdigit, student.mobile_number))

        # Format the phone number with the country code (e.g., for India)
        formatted_to_number = '+91 ' + to_number

        try:
            message = client.messages.create(
                to=formatted_to_number,
                from_= Tfrom,  # Replace with your Twilio number
                body=message
            )
        except Exception as e:
            # Handle the error, e.g., log it for debugging
            print(f"Twilio Error: {str(e)}")

    if request.method == 'POST':
        fee_form = FeeForm(request.POST)
        if fee_form.is_valid():
            with transaction.atomic():
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

                # Calculate total paid amount including advance payment
                total_paid_amount = (
                    fee.registration_fee + fee.tuition_fee + fee.exam_fee +
                    fee.sports_fee + fee.miscellaneous_fee - fee.discount_fee + fee.late_fee
                )
                fee.total_paid_amount = total_paid_amount

                fee.semester = student.current_semester

                fee.total_amount_in_words = num2words(total_paid_amount, lang='en_IN').title()

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
                
                if remaining_amount < 0:
                     fee.advance_payment = abs(remaining_amount)
                     fee.remaining_amount = 0
                else:
                    fee.advance_payment = 0
                    fee.remaining_amount = remaining_amount

                # Adjust remaining amount based on advance fee payment for subsequent semesters
                current_semester = int(current_semester)

                # Check if the current semester is greater than 1
                if current_semester > 1:
                    # Calculate the total advance amount from previous semesters, including the current semester
                    advance_amount_from_previous_semesters = sum(total_paid_amount_history.get(semester, 0) for semester in range(1, current_semester + 1))
                    # Adjust remaining amount by subtracting the advance amount
                    remaining_amount -= advance_amount_from_previous_semesters

                # Ensure remaining amount is non-negative
                remaining_amount = max(0, remaining_amount)

                # Create a thread to send the message in the background
                message_thread = threading.Thread(target=send_message_background(total_paid_amount, current_semester, remaining_amount))
                message_thread.start()

                fee.save()

                return redirect('generate_receipt', fee_id=fee.id)
        else:
            print(fee_form.errors)

    else:
        fee_form = FeeForm() 

    return render(request, 'fee_management/fee_submission.html', {'fee_form': fee_form, 'student': student})


@login_required
@allowed_users(allowed_roles=['admin'])
def generate_receipt(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id)
    student = fee.student
    context = {
        'student': student,
        'fee': fee,
        'remaining_due': fee.remaining_amount,
        'advance_payment': fee.advance_payment
    }

    return render(request, 'fee_management/receipt.html', context)


@login_required
@allowed_users(allowed_roles=['admin'])
def fee_history(request, student_id):
    student = get_object_or_404(AdmissionForm, id=student_id)  # Get the student by ID

    # Query the database to get the fee history for the selected student
    fee_history = Fee.objects.filter(student=student).order_by('-payment_date')

    # Configure the pagination
    page = request.GET.get('page')
    paginator = Paginator(fee_history, 10)  # Show 10 fee entries per page

    try:
        fee_history = paginator.page(page)
    except PageNotAnInteger:
        fee_history = paginator.page(1)
    except EmptyPage:
        fee_history = paginator.page(paginator.num_pages)
    
    return render(request, 'fee_management/fee_history.html', {'student': student, 'fee_history': fee_history})

@login_required
@allowed_users(allowed_roles=['admin'])
def send_message(request, student_id, remaining_amount):
    student = get_object_or_404(AdmissionForm, id=student_id)

    # Sanitize the phone number (remove non-numeric characters)
    to_number = ''.join(filter(str.isdigit, student.mobile_number))

    # Format the phone number with the country code (e.g., for India)
    formatted_to_number = '+91 ' + to_number

    # Define the message to send
    message = f"प्रिय छात्र/छात्रा {student.first_name}, यह संदेश चन्द्रिका प्रसाद महाविद्यालय से है | आपका {remaining_amount } रुपये भुगतान शेष है | कृपया जल्द से जल्द भुगतान करें।"

    # Use Twilio to send the message
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    try:
    
        message = client.messages.create(
            to=formatted_to_number,
            from_= Tfrom,
            body=message
        )
        return HttpResponse("Message sent successfully!")
    except Exception as e:
        # Handle the error, e.g., log it for debugging
        print(f"Twilio Error: {str(e)}")
        return HttpResponse("Error sending the message.")


@login_required
@allowed_users(allowed_roles=['admin'])
def fee_dashboard(request):
    today = timezone.now().date()

    # Calculate the start and end of the current week
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Calculate the start and end of the current month
    start_of_month = today.replace(day=1)
    end_of_month = start_of_month.replace(day=28) + timedelta(days=4)
    end_of_month = end_of_month - timedelta(days=end_of_month.day)

    # Calculate the start and end of the current year
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)

    # Query the database to get the relevant fee data
    today_fee_collection = Fee.objects.filter(payment_date=today).aggregate(Sum('total_paid_amount'))['total_paid_amount__sum'] or 0
    weekly_fee_collection = Fee.objects.filter(payment_date__range=[start_of_week, end_of_week]).aggregate(Sum('total_paid_amount'))['total_paid_amount__sum'] or 0
    monthly_fee_collection = Fee.objects.filter(payment_date__range=[start_of_month, end_of_month]).aggregate(Sum('total_paid_amount'))['total_paid_amount__sum'] or 0
    yearly_fee_collection = Fee.objects.filter(payment_date__range=[start_of_year, end_of_year]).aggregate(Sum('total_paid_amount'))['total_paid_amount__sum'] or 0

    return render(request, 'fee_management/fee_dashboard.html', {
        'today_fee_collection': today_fee_collection,
        'weekly_fee_collection': weekly_fee_collection,
        'monthly_fee_collection': monthly_fee_collection,
        'yearly_fee_collection': yearly_fee_collection,
    })

@login_required
@allowed_users(allowed_roles=['admin'])
def fee_dashboard_api(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_of_month = today.replace(day=1)
    end_of_month = start_of_month.replace(day=28) + timedelta(days=4)
    end_of_month = end_of_month - timedelta(days=end_of_month.day)
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)

    today_fee_entries = Fee.objects.filter(payment_date=today)
    weekly_fee_entries = Fee.objects.filter(payment_date__range=[start_of_week, end_of_week])
    
    # Aggregate monthly data for all months
    monthly_fee_entries = Fee.objects \
        .annotate(month=TruncMonth('payment_date')) \
        .values('month') \
        .annotate(total_amount=Sum('total_paid_amount')) \
        .order_by('month')

    # Aggregate yearly data for all years
    yearly_fee_entries = Fee.objects \
        .annotate(year=TruncYear('payment_date')) \
        .values('year') \
        .annotate(total_amount=Sum('total_paid_amount')) \
        .order_by('year')
    
    yearly_fee_collection = dict((entry['year'].strftime('%Y'), float(entry['total_amount'])) for entry in yearly_fee_entries)

    # Convert Decimal values to float before serializing
    today_fee_entries_json = serialize('json', today_fee_entries, use_natural_primary_keys=True)


    # Aggregate weekly data
    weekly_data = {}
    for entry in weekly_fee_entries:
        payment_date = entry.payment_date.strftime('%A')  # Get the day of the week
        if payment_date not in weekly_data:
            weekly_data[payment_date] = 0
        weekly_data[payment_date] += entry.total_paid_amount



    response_data = {
        'today_fee_entries': json.loads(today_fee_entries_json),
        'weekly_fee_entries': weekly_data,
        'monthly_fee_collection': dict((entry['month'].strftime('%B'), entry['total_amount']) for entry in monthly_fee_entries),
        'yearly_fee_collection': yearly_fee_collection,
    }

    return JsonResponse(response_data)