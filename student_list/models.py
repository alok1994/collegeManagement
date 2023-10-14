from django.db import models
from admissionapp.models import AdmissionForm  # Import the AdmissionForm model from admissionapp

class Student(models.Model):
    admission_form = models.ForeignKey(AdmissionForm, on_delete=models.CASCADE)
    # Add any additional fields you want to display in the list

    def __str__(self):
        return f"{self.admission_form.first_name} {self.admission_form.last_name}"
