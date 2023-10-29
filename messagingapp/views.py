# messagingapp/views.py
from django.shortcuts import render, redirect
from .forms import MessageForm
from admissionapp.models import AdmissionForm
from twilio.rest import Client
from django.conf import settings 
from django.shortcuts import render
from django.http import HttpResponse
import logging


'''def send_messages(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']
            message_text = form.cleaned_data['message_text']

            students = AdmissionForm.objects.filter(current_semester=semester)
            for student in students:
                send_twilio_message(student.mobile_number, message_text)  # Send the message

            return redirect('message_sent')  # Redirect to a confirmation page
    else:
        form = MessageForm()

    return render(request, 'messagingapp/send_messages.html', {'form': form})'''

def send_messages(request):
    messages_sent = False  # Variable to indicate whether messages were sent

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']
            message_text = form.cleaned_data['message_text']

            students = AdmissionForm.objects.filter(current_semester=semester)
            for student in students:
                send_twilio_message(student.mobile_number, message_text)  # Send the message

            messages_sent = True  # Set the variable to True

    else:
        form = MessageForm()

    return render(request, 'messagingapp/send_messages.html', {'form': form, 'messages_sent': messages_sent})


def send_twilio_message(to_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # Format the phone number with the country code (e.g., for India)
    formatted_to_number = '+91' + to_number
    try:
        message = client.messages.create(
            to=formatted_to_number,
            from_='+13348304110',  # Replace with your Twilio number
            body=message
        )
    except Exception as e:
        # Handle the error, e.g., log it for debugging
        print(f"Twilio Error: {str(e)}")


def message_sent(request):
    logger = logging.getLogger(__name__)
    logger.info('Messages sent successfully.')
    return render(request, 'messagingapp/message_sent.html')